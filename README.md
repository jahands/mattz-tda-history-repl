# View history in browser
https://mattz-history.geostyx.com/

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