from neo4j import GraphDatabase, basic_auth


class Neo4jClient:
    def __init__(self):
        self.driver = GraphDatabase.driver("bolt://54.157.51.12:7687",auth=basic_auth("neo4j", "diagnosis-section-conversions"))

    def close(self):
        self.driver.close()    
        
    def run_query(self, query):
        with self.driver.session() as session:
            result = list(session.run(query))
            return result




def quem_faz_academia(client):
    query = "MATCH (p:Pessoa) - [:TEM_COMO_HOBBY]->(:Hobby {nome: 'Academia'}) RETURN p.nome AS nome"
    result = client.run_query(query)
    return [record["nome"] for record in result] 

def quem_tem_pet(client):
    query = "MATCH (p:Pessoa) - [:DONO_DE]->(:Pet) RETURN p.nome AS nome"
    result = client.run_query(query)
    return [record["nome"] for record in result] 

def quem_nao_mora_em_MG(client):
    query = "MATCH (p:Pessoa) - [:MORA_EM]->(c:Casa) WHERE NOT c.estado = 'MG' RETURN p.nome AS nome"
    result = client.run_query(query)
    return [record["nome"] for record in result] 

def quem_mora_em_sf(client):
    query = "MATCH (p:Pessoa) - [:MORA_EM]->(c:Casa) WHERE c.cidade = 'Sao Francisco' RETURN p.nome AS nome"
    result = client.run_query(query)
    return [record["nome"] for record in result] 



client = Neo4jClient()

ratosDeAcademia = quem_faz_academia(client)
print("Os maromba da familia: ", ratosDeAcademia)

paiDePet = quem_tem_pet(client)
print("Pai de Pet da familia e: ", paiDePet)

foraDeMG = quem_nao_mora_em_MG(client)
print("Quem mora fora de MG: ", foraDeMG)

sf = quem_mora_em_sf(client)
print("Quem mora em SF: ", sf)