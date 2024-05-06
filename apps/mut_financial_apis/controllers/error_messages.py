class FinanceApiErrorMessages:
    COMPANY_NOT_FOUND = {
        "code": "01",
        "message": "No Company was found for the given 'cnpj_singular'!"
    }
    INVALID_CNPJ_CPF = {
        "code": "02",
        "message": "The payer's CNPJ/CPF is invalid!"
    }
    INVALID_EMAIL = {
        "code": "03",
        "message": "The payer's e-mail is invalid!"
    }
