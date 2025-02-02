import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
import string
wnl = nltk.WordNetLemmatizer()
from sentiwordnet import SentiWordNetCorpusReader, SentiSynset

wntags = ["N","R","V"]
wnltags = ["n","r","v","a"]
fdom = ['accountancy.n.01','accounting.n.02','auction.n.02','banking.n.01',
'banking.n.02','business.n.07','business.n.01','commerce.n.01','commercial_enterprise.n.02',
'contract.n.01','corporate_finance.n.01','corporation.n.01','corporation_law.n.01',
'economics.n.01','finance.n.02','growth.n.01','investing.n.01',
'investment.n.02','stock_exchange.n.01','tax.n.01','trade.n.01']

financewords = ["accounting",
"accrue",
"accumulate",
"acquisition",
"activity",
"adjustable",
"adjustment",
"amortization",
"annuity",
"appraisal",
"arbitrage",
"arrangement",
"arrears",
"assets",
"authentic",
"authorization",
"automated",
"average",
"averaging",
"bankrupt",
"barter",
"bear",
"beneficiary",
"bid",
"bracket",
"broker",
"brokerage",
"bull",
"buying",
"buyout",
"cartel",
"cashier",
"certificate",
"certified",
"churn",
"circulation",
"clearinghouse",
"collateral",
"collect",
"commission",
"commodity",
"compensation",
"competitor",
"compound",
"conglomerate",
"consolidation",
"consortium",
"consumer",
"convertible",
"correction",
"countersign",
"credit",
"currency",
"custodian",
"debit",
"debt",
"deductible",
"deduction",
"default",
"delinquency",
"demand",
"depository",
"depreciation",
"depression",
"deregulation",
"designation",
"devaluation",
"differential",
"discount",
"distribution",
"diversify",
"dividend",
"downturn",
"draft",
"driven",
"electronic",
"elimination",
"embezzlement",
"endorse",
"enterprise",
"entity",
"equity",
"escrow",
"ESOP",
"estimation",
"evaluation",
"exceed",
"exorbitant",
"expectation",
"extortion",
"federal",
"fees",
"fiduciary",
"finance",
"fiscal",
"fixed",
"float",
"foreclosure",
"forfeiture",
"frugality",
"fulfillment",
"fund",
"funds",
"futures",
"government",
"growth",
"guarantee",
"guaranty",
"illegal",
"imprint",
"income",
"index",
"industrials",
"insolvent",
"installment",
"institution",
"insufficient",
"intangible",
"interest",
"interest-bearing",
"intermediary",
"intervention",
"invalidate",
"investment",
"IRA",
"issue",
"kiting",
"leverage",
"liability",
"lien",
"liquidity",
"long-term",
"lucrative",
"margin",
"market",
"maturity",
"mercantile",
"merger",
"monopoly",
"municipals",
"non-speculative",
"NYSE",
"operation",
"option",
"overcompensate",
"oversight",
"ownership",
"payment",
"percent",
"planning",
"pledge",
"portfolio",
"practice",
"predetermine",
"premium",
"principal",
"product",
"profit",
"progressive",
"public",
"qualm",
"quantity",
"questionable",
"quick",
"quittance",
"ramification",
"rate",
"recession",
"record",
"recoup",
"recourse",
"redemption",
"reduction",
"regulation",
"reimburse",
"reliability",
"reserves",
"retirement",
"risk",
"securities",
"select",
"selling",
"sell-off",
"shares",
"shylock",
"slump",
"solvency",
"speculate",
"speculative",
"split",
"stagflation",
"stocks",
"subscription",
"summary",
"surety",
"surplus",
"survivorship",
"swap",
"technical",
"tender",
"thrifts",
"transaction",
"transfer",
"transferable",
"underwriter",
"unit",
"unofficial",
"unregulated",
"unsecured",
"untaxed",
"usury",
"utilities",
"value",
"variable",
"vault",
"venture",
"void",
"voucher",
"warrant",
"wide-ranging",
"withdrawal",
"account",
"accountancy",
"accounting",
"accumulation",
"administration",
"analysis",
"analyst",
"antique",
"article",
"auction",
"balance",
"banking",
"bankroll",
"bearish",
"bond",
"broken",
"bullish",
"business",
"buy",
"by-bid",
"calculation",
"capital",
"capitalist",
"carry",
"case",
"casestudy",
"chain",
"charge",
"clear",
"closing",
"collector",
"commerce",
"commercial",
"commercialize",
"comparison-shop",
"consumption",
"contract",
"copartner",
"corporate",
"corporation",
"coupon",
"deaccession",
"deal",
"debenture",
"deflationary",
"disposable",
"dull",
"easy",
"economic",
"economics",
"economy",
"establishment",
"estate",
"exchange",
"expense",
"export",
"failure",
"film",
"foist",
"franchise",
"fundamental",
"gambling",
"GDP",
"get",
"greenmail",
"gresham's",
"gross",
"handshake",
"high-interest",
"hostile",
"identification",
"import",
"imposition",
"impulse-buy",
"incorporate",
"inflationary",
"inventory",
"invested",
"investing",
"isometry",
"judgment",
"laundering",
"law",
"long",
"loophole",
"maintain",
"marginal",
"monopsony",
"moral",
"mortmain",
"negociate",
"negotiable",
"net",
"nominal",
"obligation",
"offer",
"offset",
"oligopoly",
"outbid",
"over",
"overbid",
"overcapitalization",
"pawn",
"personam",
"pick",
"player",
"price",
"price-to-earnings",
"privatize",
"production",
"productivity",
"protect",
"pyramid",
"quaestor",
"quality",
"rally",
"ratio",
"real",
"realize",
"regressive",
"remainder",
"renegociate",
"resell",
"retail",
"return",
"review",
"right",
"rubber",
"savings",
"sell",
"shipping",
"shop",
"short",
"shrewdness",
"smuggle",
"spillover",
"stagnation",
"stock",
"subscribe",
"subscribed",
"take",
"takeover",
"tangible",
"tax",
"terminated",
"tight",
"trade",
"traffic",
"transact",
"trust",
"turn",
"unbalanced",
"unbroken",
"uncollected",
"underbid",
"unearned",
"usance",
"utility",
"valuable",
"wage",
"wholesale",
"withholding",
"write-off",
"yield"
]
fdomset = set(fdom)
financewordset = set(financewords)

def isPunct(word):
  return len(word) == 1 and word in string.punctuation

def isNumeric(word):
  try:
    float(word) if '.' in word else int(word)
    return True
  except ValueError:
    return False

def isStopWord(word):
    return (word.lower() in nltk.corpus.stopwords.words('english'))    


def finddomain(tok):  
    filtered_words = [w for w in tok if not(isPunct(w[0]) or isNumeric(w[0]) or isStopWord(w[0]))]
    toklem = [wnl.lemmatize(a.lower()) if a!="have" and a!="has" else "have" for a in filtered_words]
    domainsyn = []
    domain = []
    fincount = 0.0
##    flag = False
    for i in toklem:
        if i in  financewordset:
            fincount = fincount + 1.0
##            flag = True
        for j in wnltags:
            isyn = wn.synsets(i,j)
            for s in isyn:
                domainsyn.extend(s.topic_domains())
##                if not(flag):
##                    for u in s.lemmas:
##                        if not(flag):
##                            for v in u.derivationally_related_forms():
##                                if v.name in financewordset and not(flag):
##                                    fincount = fincount + 1.0
##                                    flag = True
##                                    break
##        flag = False
    for p in domainsyn:
        domain.append(p.name)
    total = len(domain)
    sum = 0.0
    for elem in domain:
        if elem in fdomset:
            sum = sum+1.0
    totalwords = len(toklem)
    #print sum, total, fincount, totalwords
    if total==0:
        r1=0
    else:
        r1 = sum/total
    if totalwords==0:
        r2=0
    else:
        r2 = fincount/totalwords
    return (r1+r2)/2.0
        
        
    
    
    
