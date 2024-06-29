use sqlx::{
    postgres::{PgConnectOptions, PgPoolOptions},
    PgPool,
};
use tokio::sync::OnceCell;

use crate::{environment::env_vars::ENV_VARS, simdata_types::simdata_result::SimData};

pub async fn get_simdata(b: f32, f: f32, g: f32) -> Vec<SimData> {
    let rows: Vec<SimData> = sqlx::query_as("SELECT * FROM simresults WHERE b=0 AND f=1 AND g=2")
        .bind(b)
        .bind(f)
        .bind(g)
        .fetch_all(&get_pool().await)
        .await
        .unwrap();

    rows
}

pub async fn get_pool() -> PgPool {
    let pool = POOL
        .get_or_init(|| async {
            let options = PgConnectOptions::new()
                .host(&ENV_VARS.db_url)
                .port(5432)
                .database(&ENV_VARS.db_name);
            PgPoolOptions::new()
                .max_connections(1024)
                // .max_lifetime(Duration::from_secs(1))
                .connect_with(options)
                .await
                .expect("asd")
        })
        .await
        .clone();
    return pool;
}

static POOL: OnceCell<PgPool> = OnceCell::const_new();
