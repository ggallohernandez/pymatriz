
authenticate = "https://matriz.auth0.com/co/authenticate"
authorize = "https://matriz.auth0.com/authorize?client_id={client_id}&response_type={response_type}" \
            "&response_mode={response_mode}&redirect_uri={redirect_uri}&connection={connection}" \
            "&scope={scope}&realm={realm}&login_ticket={login_ticket}&auth0Client={auth0_client}"

instruments = "api/v1/platform/market/seclist"
market_data = "api/v1/platform/market/md"

historical_series_daily = "api/v1/platform/series/daily?sid={instrument}&from={start_date}&to={end_date}"
historical_series_intraday = "api/v1/platform/series/intraday?sid={instrument}&from={start_date}&to={end_date}"

ws_request = "ws?token={token}&cid={connection_id}&account={account}"
ws_subscribe = "api/v1/platform/subscriptions?token={token}&cid={connection_id}"
