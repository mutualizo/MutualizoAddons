class FinanceApiErrorMessages:
    MISSING_EXTERNAL_ID = {
        "code": "00",
        "message": "The field 'external_id' is required!"
    }
    COMPANY_NOT_FOUND = {
        "code": "01",
        "message": "No Company was found for the given 'cnpj_singular'!"
    }
    INVALID_CNPJ_CPF = {
        "code": "02",
        "message": "The payer's CNPJ/CPF is invalid!"
    }
    INVALID_DUE_DATE = {
        "code": "03",
        "message": "The installment due date is invalid! The correct date format is 'yyyy-mm-dd'."
    }
    INVALID_INSTALLMENT_AMOUNT = {
        "code": "04",
        "message": "The installment amount is invalid! Please use . as decimal separator."
    }
    INVALID_EMAIL = {
        "code": "05",
        "message": "The payer's e-mail is invalid!"
    }
    PAYMENT_MODE_NOT_FOUND = {
        "code": "06",
        "message": "The payment configuration is not set for the given 'cnpj_singular'"
    }
