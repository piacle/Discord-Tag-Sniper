from asyncio import run, sleep
from PyTerm import Console
from httpx import AsyncClient
from threading import Thread
class DiscordTagSniper:
    def __init__(self) -> None:
        self.requests, self.ratelimits, self.errors, self.claimed, self.tokens, self.main_token, self.password, self.tag, self.client, self.uid = 0, 0, 0, False, open(input("[^] Path for tha tokens > ")).readlines(), input("[^] Your main token > "), input("[^] Your password > "), input("[^] Their tag > "), AsyncClient(), input("[^] Their ID > ")
        self.username, self.discriminator = self.tag.split("#")[0], self.tag.split("#")[1]

    async def set_title(self):
        while self.claimed is False:
            Console.set_title(f"Discord Tag Sniper | Requests: {self.requests} | Ratelimits: {self.ratelimits} | Errors: {self.errors}")

    async def claim_user(self):
        r = await self.client.post(
            url = "https://discord.com/api/v9/users/@me",
            headers = {
                "Authorization": self.main_token
            },
            data = {
                "username": self.username, 
                "password": self.password, 
                "discriminator": self.discriminator
            }
        )

        if r.status_code == 200:
            self.requests += 1
            self.claimed = True
            print(f"[+] Sniped Tag: {self.tag} | Requests: {self.requests} | Ratelimits: {self.ratelimits} | Errors: {self.errors}")
        elif r.status_code == 429:
            self.ratelimits += 1
        else:
            self.errors += 1
            print(f"[-] {r.json()}")


    async def check_user(self):
        while self.claimed is False:
            for token in self.tokens:
                r = await self.client.get(
                    url = f"https://discord.com/api/v9/users/{self.uid}", 
                    headers = {
                        "Authorization": token
                    })
                self.requests += 1
                json = r.json()
                
                if (r.status_code == 200):
                    if (json["username"] != self.username or json["discriminator"] != self.discriminator):
                        await self.claim_user()
                elif r.status_code == 429:
                    self.ratelimits += 1
                    await sleep(json['retry_after'] + .5)
                else:
                    self.errors += 1
                

if __name__ == "__main__":
    a = DiscordTagSniper()
    t = int(input("[^] Threads > "))
    Console.clear()
    Thread(target=run, args=[a.set_title()], daemon=True).start()
    [Thread(target=run, args=[a.check_user()], daemon=True).start() for _ in range(t)]
    while True:
        if a.claimed == True:
            break
        else:
            pass