resource "google_sql_database_instance" "redaction" {
  name             = "redaction-pg"
  database_version = "POSTGRES_16"
  region           = var.region

  settings {
    tier    = "db-custom-1-3840"
    edition = "ENTERPRISE"
  }
}

resource "google_sql_database" "redaction" {
  name     = "redaction"
  instance = google_sql_database_instance.redaction.name
}

resource "google_sql_user" "redact" {
  name     = "redact"
  instance = google_sql_database_instance.redaction.name
  password = var.redaction_db_password # prefer injecting at apply time, not hardcoding
}
