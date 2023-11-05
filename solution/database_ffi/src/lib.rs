use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;
use database_lib::Database as RustDatabase;

#[pyclass]
struct Database(RustDatabase);

#[pymethods]
impl Database {
    #[new]
    fn new() -> PyResult<Self> {
        Ok(Database(RustDatabase::load().map_err(|e| PyValueError::new_err(e.to_string()))?))
    }

    fn get_edges(&self, from_id: i64, edge_id: i64) -> Vec<i64> {
        self.0.get_edges(from_id, edge_id)
    }

    fn two_hops(&self, from_id: i64, edge1_type: i64, edge2_type: i64) -> Vec<i64> {
        self.0.two_hops(from_id, edge1_type, edge2_type)
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn database_ffi(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Database>()?;
    Ok(())
}
