use serde::{Deserialize, Serialize};
use std::collections::{HashMap, HashSet};
use std::fs::File;

// TODO: Make this relative to the repo or an absolute path
const DB_PATH: &str = "../data.json";

type ObjectId = i64;
type RawEdge = (i64, i64);
type EdgeType = i64;

#[derive(Serialize, Deserialize, Debug, PartialEq, Eq)]
enum Bidir {
    Bidir,
    Single,
}

#[derive(Serialize, Deserialize, Debug)]
struct EdgeInfo {
    bidir: Bidir,
    edges: Vec<RawEdge>,
}

type RawDatabase = HashMap<EdgeType, EdgeInfo>;

#[derive(Debug)]
pub struct Database {
    data: HashMap<i64, ObjectData>,
}

#[derive(Debug, Default)]
struct ObjectData {
    edges: HashMap<EdgeType, HashSet<ObjectId>>,
}

impl Database {
    pub fn load() -> Result<Self, anyhow::Error> {
        let file = File::open(DB_PATH)?;
        let raw_db: RawDatabase = serde_json::from_reader(file)?;
        let mut data: HashMap<ObjectId, ObjectData> = HashMap::new();
        for (edge_type, edge_info) in raw_db {
            for (from, to) in edge_info.edges {
                data.entry(from)
                    .or_default()
                    .edges
                    .entry(edge_type)
                    .or_default()
                    .insert(to);
                if edge_info.bidir == Bidir::Bidir {
                    data.entry(to)
                        .or_default()
                        .edges
                        .entry(edge_type)
                        .or_default()
                        .insert(from);
                }
            }
        }
        Ok(Self { data })
    }

    pub fn get_edges(&self, from: ObjectId, edge_type: EdgeType) -> Vec<ObjectId> {
        let mut edges: Vec<_> = match self.data.get(&from).and_then(|data| data.edges.get(&edge_type)) {
            Some(edges) => edges.iter().copied().collect(),
            None => return Vec::new(),
        };
        edges.sort();
        edges

    }

    pub fn two_hops(&self, from: ObjectId, edge1_type: EdgeType, edge2_type: EdgeType) -> Vec<ObjectId> {
        let mut result = HashSet::new();
        for adj in self.get_edges(from, edge1_type) {
            result.extend(self.get_edges(adj, edge2_type));
        }
        let mut result: Vec<_> = result.into_iter().collect();
        result.sort();
        result
    }
}