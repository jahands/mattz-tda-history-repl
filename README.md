# View history in browser
https://mattz-history.geostyx.com/

runs 6 as of 2/21
[Notion page](https://www.notion.so/jhands/mattz-test-for-b2-api-calls-3028f637f9024b79b78f6e36812ec1fe)

this is running on apps-log (byobu)
`rclone serve http b2-cache:`

`caddy run`

Caddyfile:
```Caddyfile
{
	email jacob@gogit.io
}
mattz-history.geostyx.com {
	tls {
		dns cloudflare xxx
	}
	reverse_proxy /* localhost:8080
}
```