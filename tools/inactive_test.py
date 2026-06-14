import asyncio
import random
from pathlib import Path

import aiodns
import aiohttp

DOMAINS_FILE = Path("logs/domains.txt")
OUTPUT_FILE = Path("logs/inactive_domains_test.log")

# Tune these for safety on GitHub Actions
MAX_CONCURRENT = 50          # keep this modest to avoid DNS throttling
DNS_TIMEOUT = 0.5            # seconds
HTTP_TIMEOUT = 2.0           # seconds
JITTER_MAX = 0.05            # up to 50ms random delay per task


resolver = aiodns.DNSResolver(timeout=DNS_TIMEOUT)


async def dns_has_records(domain: str) -> bool:
    # Only A, NS, SOA to reduce DNS traffic
    for rtype in ("A", "NS", "SOA"):
        try:
            await resolver.query(domain, rtype)
            return True
        except Exception:
            continue
    return False


async def http_reachable(domain: str, session: aiohttp.ClientSession) -> bool:
    for proto in ("http://", "https://"):
        url = proto + domain
        try:
            async with session.head(url, timeout=HTTP_TIMEOUT, allow_redirects=True) as resp:
                if resp.status < 500:
                    return True
        except Exception:
            continue
    return False


async def is_inactive(domain: str, session: aiohttp.ClientSession) -> bool:
    # 1) DNS check
    if await dns_has_records(domain):
        return False

    # 2) HTTP reachability
    if await http_reachable(domain, session):
        return False

    # No DNS + no HTTP → treat as inactive
    return True


async def main():
    if not DOMAINS_FILE.exists():
        print(f"{DOMAINS_FILE} does not exist, nothing to do.")
        return

    with DOMAINS_FILE.open() as f:
        domains = [line.strip() for line in f if line.strip()]

    sem = asyncio.Semaphore(MAX_CONCURRENT)
    inactive_domains = []

    async with aiohttp.ClientSession() as session:
        async def worker(domain: str):
            # Small jitter to avoid DNS bursts
            await asyncio.sleep(random.uniform(0, JITTER_MAX))
            async with sem:
                try:
                    dead = await is_inactive(domain, session)
                    if dead:
                        inactive_domains.append(domain)
                except Exception:
                    # On any unexpected error, just skip this domain
                    pass

        await asyncio.gather(*(worker(d) for d in domains))

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w") as f:
        for d in inactive_domains:
            f.write(d + "\n")


if __name__ == "__main__":
    asyncio.run(main())
