from repository.schema import Server
import httpx


async def is_healthy(server: Server):
    async with httpx.AsyncClient() as client:
        try:
            req = build_url(server.ip)
            response = await client.get(req)
            if not 500 <= response.status_code <= 599:
                print("success: ", req)
                return True
            else:
                print("failed: ", req)
                return False
        except Exception:
            print("failed: ", req)
            return False


def build_url(ip: str):
    return "http://" + ip
