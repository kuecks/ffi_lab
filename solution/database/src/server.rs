use tonic::{transport::Server, Request, Response, Status};

use database::database_server::{Database as DatabaseTrait, DatabaseServer};
use database::{GetEdgesRequest, GetEdgesResponse, TwoHopsRequest};
use database_lib::Database;

pub mod database {
    tonic::include_proto!("database");
}

#[derive(Debug)]
pub struct DatabaseImpl {
    db: Database,
}

#[tonic::async_trait]
impl DatabaseTrait for DatabaseImpl {
    async fn get_edges(&self, request: Request<GetEdgesRequest>) -> Result<Response<GetEdgesResponse>, Status> {
        println!("Received request: {:?}", request);
        let request = request.into_inner();
        let ids = self.db.get_edges(request.from_id, request.edge_type);
        Ok(Response::new(GetEdgesResponse { ids }))
    }

    async fn two_hops(&self, request: Request<TwoHopsRequest>) -> Result<Response<GetEdgesResponse>, Status> {
        let request = request.into_inner();
        let ids = self.db.two_hops(request.from_id, request.edge1_type, request.edge2_type);
        Ok(Response::new(GetEdgesResponse { ids }))
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let addr = "[::1]:50051".parse()?;
    let database = DatabaseImpl { db: Database::load()? };

    Server::builder()
        .add_service(DatabaseServer::new(database))
        .serve(addr)
        .await?;

    Ok(())
}