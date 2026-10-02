# Application contract

jsonwebtoken verify is the standard implementation. trustedPublicKey comes from server config, not token input. Issuer always supplies expiry and the application accepts only these access tokens. Key rotation and session revocation are outside this isolated helper scope.
