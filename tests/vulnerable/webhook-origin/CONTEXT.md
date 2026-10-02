# Application contract

Public webhook with parsed JSON and no middleware or gateway signature check. Provider requires a signature; only verified events may mark orders paid. markPaid changes the order state without further validation.
