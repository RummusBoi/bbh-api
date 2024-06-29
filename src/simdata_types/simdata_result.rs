#[derive(sqlx::FromRow, Debug)]
pub struct SimData {
    pub endstate: i32,
    pub n_ims: i32,
    pub d_min: f32,
    pub e_bs: f32,
}
