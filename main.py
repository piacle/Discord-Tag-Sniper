import httpx
import asyncio
import PyTerm

class DiscordTagSniper:
    def __init__(self) -> None:
        self.attempts = 0

        self.token = str(input("Discord Token: "))
        self.password = str(input("Discord Password: "))
        self.tag = str(input("Target's Discord Tag: "))
        self.user_id = int(input("Target's Discord User ID: "))

        self.username = self.tag.split("#")[0]
        self.discriminator = self.tag.split("#")[-1]

        self.client = httpx.AsyncClient()
        self.client.headers = {"Authorization": self.token} 

    async def claim_user(self):
        r = await self.client.post(
            url = "https://discord.com/api/v9/users/@me",
            data = {
                "username": self.username, 
                "password": self.password, 
                "discriminator": self.discriminator
            }
        )

        if r.status_code == 200:
            self.attempts += 1
            print(f"[+] Sniped Tag: {self.tag} | Tries: {self.attempts}")
            PyTerm.Console.set_title(f"Discord Tag Sniper | Tries: {self.attempts}")
            print("Press any key to exit...")
            PyTerm.Console.get_char()
        elif r.status_code == 400:
            self.attempts += 1
            PyTerm.Console.set_title(f"Discord Tag Sniper | Tries: {self.attempts}")
        else:
            self.attempts += 1
            print(f"[-] {r.json()}")
            PyTerm.Console.set_title(f"Discord Tag Sniper | Tries: {self.attempts}")


    async def check_user(self):
        r = await self.client.get(f"https://discord.com/api/v9/users/{self.user_id}")
        r = r.json()
        return (r["username"], r["discriminator"])

    async def start(self):
        while True:
            info = await self.check_user()
            if info[0] != self.username or info[1] != self.discriminator:
                await self.claim_user()

if __name__ == "__main__":
    asyncio.run(DiscordTagSniper().start())
