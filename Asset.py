from Action import *

class AssetType:

    #assets
    cash = 0
    bond = 1
    stock = 2
    ira_stock = 3
    ira_bond = 4
    ira_cash = 19
    qtp_stock = 5
    qtp_bond = 6
    qtp_cash = 20
    
    #spending
    spend_taxes_state = 7
    spend_taxes_federal = 17
    spend_taxes_penalty = 18
    spend_living_expenses = 8
    spend_down_payment_on_house = 9
    spend_mortgage_payment_on_house = 10
    spend_kids_college_tuition = 11
    spend_kids_college_edu = 12
    spend_kids_college_misc = 13
    spend_kids_expenses = 14

    #indecies
    index_cost_of_living = 15
    index_college_tuition = 16



LIST_OF_ALL_ASSET_TYPES = [AssetType.cash,AssetType.bond,AssetType.stock,AssetType.ira_stock,AssetType.ira_cash, AssetType.qtp_cash, AssetType.ira_bond,AssetType.qtp_stock,AssetType.qtp_bond,AssetType.spend_taxes_state,AssetType.spend_taxes_federal,AssetType.spend_taxes_penalty,AssetType.spend_living_expenses,AssetType.spend_down_payment_on_house,AssetType.spend_mortgage_payment_on_house,AssetType.spend_kids_college_tuition,AssetType.spend_kids_college_edu,AssetType.spend_kids_college_misc,AssetType.spend_kids_expenses ,AssetType.index_cost_of_living,AssetType.index_college_tuition]

LIST_OF_ASSET_TYPES = [AssetType.cash,AssetType.bond,AssetType.stock,AssetType.ira_stock,AssetType.qtp_cash,AssetType.ira_cash, AssetType.ira_bond,AssetType.qtp_stock,AssetType.qtp_bond]
LIST_OF_SINK_TYPES = [AssetType.spend_taxes_state,AssetType.spend_taxes_federal, AssetType.spend_taxes_penalty,AssetType.spend_living_expenses,AssetType.spend_down_payment_on_house,AssetType.spend_mortgage_payment_on_house,AssetType.spend_kids_college_tuition,AssetType.spend_kids_college_edu,AssetType.spend_kids_college_misc,AssetType.spend_kids_expenses]

TAX_ADVANTAGED_ASSET_TYPES = [AssetType.ira_stock, AssetType.ira_bond, AssetType.qtp_stock, AssetType.qtp_bond, AssetType.qtp_cash,AssetType.ira_cash]

LIST_OF_IRA_TYPES = [AssetType.ira_stock, AssetType.ira_bond, AssetType.ira_cash]
LIST_OF_QTP_TYPES = [AssetType.qtp_stock, AssetType.qtp_bond, AssetType.qtp_cash]


def assetTypeToString(t):
    
    return {
    
    AssetType.cash : "cash",
    AssetType.bond : "bond",
    AssetType.stock : "stock",

    AssetType.ira_stock : "IRA stock",
    AssetType.ira_bond : "IRA bond",
    AssetType.ira_cash : "IRA cash",
    AssetType.qtp_stock : "529 stock",
    AssetType.qtp_bond : "529 bond",
    AssetType.qtp_cash : "529 cash",
    
    AssetType.spend_taxes_state : "spend on state taxes",
    AssetType.spend_taxes_federal : "spend on federal taxes",
    AssetType.spend_taxes_penalty : "spend on penalty taxes",
    AssetType.spend_living_expenses : "spend on living expenses",
    AssetType.spend_down_payment_on_house : "spend on house down payment",
    AssetType.spend_mortgage_payment_on_house : "spend on mortgage payment",
    
    AssetType.spend_kids_college_tuition : "spend on kids' college tuition",
    AssetType.spend_kids_college_edu : "spend on kids' qualified college expenses",
    AssetType.spend_kids_college_misc : "spend on kids' non-qualified college expenses",
    AssetType.spend_kids_expenses : "spend on kids' living expenses",

    AssetType.index_cost_of_living : "cost of living index",
    AssetType.index_college_tuition : "college tuition index",

}[t]
    