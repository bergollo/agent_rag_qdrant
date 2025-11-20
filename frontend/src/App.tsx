import { BrowserRouter, Routes, Route} from 'react-router-dom';
import HomePage from "./Pages/homePage";

function App() {
  return (
    <main className="min-h-screen">
      <div className="flex justify-center items-start w-full min-h-screen p-4">
        <BrowserRouter>
        {/* <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
          </ul>
          </nav> */}
          <Routes>
            <Route path="/" element={<HomePage />} />
          </Routes>
        </BrowserRouter>
      </div>
    </main>
  );
}
export default App;