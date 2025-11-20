import { test, expect } from '@playwright/test';

test.describe('Chat flow', () => {
  test('shows connection status and handles chat replies', async ({ page }) => {
    const userMessage = 'Hello from Playwright';
    let receivedQuery: string | undefined;

    await page.route('**/api/**', async (route) => {
      const url = route.request().url();

      if (url.endsWith('/api/health')) {
        return route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({ status: 'ok' }),
        });
      }

      if (url.endsWith('/api/ai/health')) {
        return route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({ status: 'ok', service: 'ai_service' }),
        });
      }

      if (url.endsWith('/api/ai/query')) {
        const body = JSON.parse(route.request().postData() ?? '{}');
        receivedQuery = body.query;

        return route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            id: 'bot-123',
            answer: 'Hello human, this is a mocked response.',
          }),
        });
      }

      // default for any other /api/*
      return route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({}),
      });
    });

    // test.setTimeout(120000);
    page.on('console', msg => console.log('PAGE CONSOLE:', msg.type(), msg.text()));
    page.on('pageerror', err => console.error('PAGE ERROR:', err.stack || err));
    page.on('requestfailed', req => console.error('REQUEST FAILED:', req.url(), req.failure()?.errorText));
    page.on('crash', () => console.error('PAGE CRASHED'));
    page.on('close', () => console.error('PAGE CLOSED EARLY'));

    try {
      await page.goto('/');
      
      // Debug: print page visible text and any Server: element(s)
      console.log('--- PAGE VISIBLE TEXT ---');
      console.log(await page.evaluate(() => document.body.innerText));
      const serverLoc = page.getByText(/Server:/);
      console.log('server element count:', await serverLoc.count());
      if (await serverLoc.count() > 0) {
        for (let i = 0; i < await serverLoc.count(); i++) {
          const el = serverLoc.nth(i);
          console.log(`server[${i}] text:`, await el.innerText());
          console.log(`server[${i}] outerHTML:`, await el.evaluate((e) => (e as HTMLElement).outerHTML));
        }
      }

      // Use a regex to allow variations like "Server: [] Connected" and wait longer
      await expect(page.getByRole('heading', { name: 'MCP React UI' })).toBeVisible();
      await expect(page.getByText('Server: Connected')).toBeVisible({ timeout: 2000 });

      const input = page.getByPlaceholder('Type a question');
      await expect(input).toBeVisible({ timeout: 5000 });
      
      // Proceed with interaction
      await input.fill(userMessage);
      await page.getByRole('button', { name: 'Send' }).click();

      await expect(page.locator('.message-bubble', { hasText: userMessage })).toBeVisible();
      await expect(page.getByText('Hello human, this is a mocked response.')).toBeVisible();
      await expect.poll(() => receivedQuery).toBe(userMessage);

    } catch (e) {
      console.error('DEBUG HTML:', await page.content().catch(() => '<could not get content>'));
      console.error('DEBUG VISIBLE:', await page.evaluate(() => document.body.innerText).catch(() => '<no text>'));
      throw e;
    }

  });
});
