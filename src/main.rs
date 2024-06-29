use axum::{
    http::StatusCode,
    routing::{get, post},
    Json, Router,
};
use bbh_api::postgres_helpers::simdata_controller::get_simdata;
use serde::{Deserialize, Serialize};

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/", get(root))
        .route("/simdata", get(getsimdata));

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

async fn root() -> &'static str {
    "Hello, World!"
}

async fn getsimdata() -> String {
    let res = get_simdata(0_f32, 1_f32, 2_f32).await;
    println!("{:?}", res);
    return String::from("hejsa");
}
