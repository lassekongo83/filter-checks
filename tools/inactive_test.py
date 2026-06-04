import asyncio
import aiodns
import aiohttp

resolver = aiodns.DNSResolver(timeout=1)

async def dns_has_records(domain):
    for rtype in ("A", "AAAA", "NS", "SOA"):
        try:
            await resolver.query(domain, rtype)
            return True
        except:
            pass
    return False

async def http_reachable(domain, session):
    for proto in ("http://", "https://"):
        try:
            async with session.head(proto + domain, timeout=2) as r:
                if r.status < 500:
                    return True
        except:
            pass
    return False

async def is_inactive(domain, session):
    if await dns_has_records(domain):
        return False
    if await http_reachable(domain, session):
        return False
    return True

async def main():
    with open("logs/domains.txt") as f:
        domains = f.read().splitlines()

    sem = asyncio.Semaphore(500)

    async with aiohttp.ClientSession() as session:
        async def worker(domain):
            async with sem:
                dead = await is_inactive(domain, session)
                return domain if dead else None

        results = await asyncio.gather(*(worker(d) for d in domains))

    with open("logs/inactive_domains_test.log", "w") as log:
        for r in results:
            if r:
                log.write(r + "\n")

asyncio.run(main())
