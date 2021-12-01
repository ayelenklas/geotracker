mkdir -p ~/.streamlit/

HEROKU_EMAIL_ADDRESS=edmondo.castoldi@protonmail.com
PORT=69420

echo "\
[general]\n\
email = \"${HEROKU_EMAIL_ADDRESS}\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml