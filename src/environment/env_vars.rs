use lazy_static::lazy_static;

pub struct EnvironmentVars {
    pub db_username: String,
    pub db_url: String,
    pub db_name: String,
}

fn generate_env_vars() -> EnvironmentVars {
    println!("Generating env vars!");
    let env_vars = read_env_vars();
    return EnvironmentVars {
        db_username: get_env_value("db_username", &env_vars).unwrap(),
        db_url: get_env_value("db_url", &env_vars).unwrap(),
        db_name: get_env_value("db_name", &env_vars).unwrap(),
    };
}

lazy_static! {
    pub static ref ENV_VARS: EnvironmentVars = generate_env_vars();
}

fn read_env_vars() -> Vec<(String, String)> {
    dotenv::from_path("./src/configuration/.env")
        .expect("Expected to find environment file at location /backend/src/configuration/.env");

    dotenv::vars().collect()
}

fn get_env_value(key: &'static str, env_vars: &Vec<(String, String)>) -> Option<String> {
    env_vars
        .iter()
        .find(|(k, _)| k == key)
        .and_then(|(_, v)| Some(v.clone()))
}
