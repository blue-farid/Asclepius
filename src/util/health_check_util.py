from src.repository.schema import Server
import httpx


async def is_healthy(server: Server):
    async with httpx.AsyncClient() as client:
        response = await client.get(build_url(server.ip))
        if response.status_code == 200:
            return True
        else:
            return False


def build_url(ip: str):
    return "http://" + ip
