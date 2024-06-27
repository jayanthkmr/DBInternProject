from __future__ import division
import operator
import nltk
import string

def isPunct(word):
  return len(word) == 1 and word in string.punctuation

def isNumeric(word):
  try:
    float(word) if '.' in word else int(word)
    return True
  except ValueError:
    return False

class RakeKeywordExtractor:

  def __init__(self):
    self.stopwords = set(nltk.corpus.stopwords.words("english"))
    self.top_fraction = 1 # consider top third candidate keywords by score

  def _generate_candidate_keywords(self, sentences):
    phrase_list = []
    for sentence in sentences:
      words = map(lambda x: "|" if x in self.stopwords else x,
        nltk.word_tokenize(sentence.lower()))
      phrase = []
      for word in words:
        if word == "|" or isPunct(word):
          if len(phrase) > 0:
            phrase_list.append(phrase)
            phrase = []
        else:
          phrase.append(word)
    return phrase_list

  def _calculate_word_scores(self, phrase_list):
    word_freq = nltk.FreqDist()
    word_degree = nltk.FreqDist()
    for phrase in phrase_list:
      degree = len(filter(lambda x: not isNumeric(x), phrase)) - 1
      for word in phrase:
        word_freq.inc(word)
        word_degree.inc(word, degree) # other words
    for word in word_freq.keys():
      word_degree[word] = word_degree[word] + word_freq[word] # itself
    # word score = deg(w) / freq(w)
    word_scores = {}
    for word in word_freq.keys():
      word_scores[word] = word_degree[word] / word_freq[word]
    return word_scores

  def _calculate_phrase_scores(self, phrase_list, word_scores):
    phrase_scores = {}
    for phrase in phrase_list:
      phrase_score = 0
      for word in phrase:
        phrase_score += word_scores[word]
      phrase_scores[" ".join(phrase)] = phrase_score
    return phrase_scores
    
  def extract(self, text, incl_scores=False):
    sentences = nltk.sent_tokenize(text)
    phrase_list = self._generate_candidate_keywords(sentences)
    word_scores = self._calculate_word_scores(phrase_list)
    phrase_scores = self._calculate_phrase_scores(
      phrase_list, word_scores)
    sorted_phrase_scores = sorted(phrase_scores.iteritems(),
      key=operator.itemgetter(1), reverse=True)
    n_phrases = len(sorted_phrase_scores)
    if incl_scores:
      return sorted_phrase_scores[0:int(n_phrases/self.top_fraction)]
    else:
      return map(lambda x: x[0],
        sorted_phrase_scores[0:int(n_phrases/self.top_fraction)])

def test():
  rake = RakeKeywordExtractor()
  keywords = rake.extract("""Stepping into a simmering controversy, BP Amoco (BPA) said Thursday that it would take a 20% stake in the initial public offering of PetroChina, China's largest oil and gas company and a subsidiary of the government's China National Petroleum Company.

BP Amoco said it would buy one-fifth of the offering for up to $1 billion and make an additional $1 billion investment in PetroChina. BP Amoco also said the two companies would jointly market fuels in eastern China.





The announcement -- as well as the Goldman Sachs roadshow aimed at selling up to 10% of PetroChina's shares on the U.S. stock market -- raised concerns among China's critics. At issue: whether the offering would signal Wall Street's tacit support of China's domestic and foreign policies. Relations between Beijing and Washington have long been clouded by China's poor record on the environment, human rights and national security matters.

A BP Amoco spokesman, Tom Koch, said the deal would help BP Amoco increase its presence in some of China's fastest-growing markets in an area the company considers to be an "immensely" important region.

And in response to questions concerning the record of the CNPC, Koch said BP Amoco would continue to "follow our policies on protecting human rights and the environment." But he could not, however, ensure that PetroChina or its state-owned parent company would meet BP Amoco's standards on those issues.

Goldman Sachs did not return a call seeking comment about its decision to underwrite the offering. Representatives for PetroChina and the Chinese government could not immediately be reached for comment.

Politicians and critics of China argue that BP Amoco or any investor that takes a stake in PetroChina can't be assured that the company is complying with U.S. standards on a host of issues.

Such concerns have set off protests as well as letter-writing campaigns to the Securities and Exchange Commission, aimed at encouraging the government body to demand more disclosure from PetroChina before approving the stock offering.

In separate letters sent last week, Sen. Sam Brownback, R-Kansas, and Rep. Spencer Bachus, R-Alabama, each implored SEC Chairman Arthur Levitt to extend the review of PetroChina for three months in order to explore the company's intended use for the IPO proceeds, as well as CNPC's dealings with rogue nations.

"CNPC has extensive dealings in countries that are currently under U.S. sanctions, such as Sudan and Iran, and American companies or persons are legally prohibited from direct or indirect business dealings with these countries to protect vital U.S. national interests," wrote Bachus, who is chairman of the monetary policy subcommittee of the banking committee.

According to Bachus and Brownback, CNPC is the largest investor in the Sudanese government's oil joint venture, the Greater Nile Petroleum Operating Company. Sudan is run by the National Islamic Front, which has been engaged in a 17-year war against its own population and is also associated with international terrorist attacks.

On Wednesday, protesters opposed to the PetroChina IPO staged a rally in New York just as Goldman Sachs was giving its presentation to potential investors.

Michelle Chan-Fishel, a policy analyst with Friends of the Earth, an environmental group that participated in the demonstration, said she believed the company was less committed to protecting the environment than other companies active in emerging markets.

She said Royal Dutch/Shell, for example, outspends PetroChina on environmental technologies in Nigeria, even though it produces only half the crude oil that PetroChina does. "Similarly," she said, "Shell Nigeria has committed 20% of its annual budget to conserve and improve the environment, compared to PetroChina's 1.5% of its capital expenditures."

Chan-Fishel said the company's prospectus did not fully disclose many of the risks inherent in investing in PetroChina.

"To what extent do American investors know the human rights, environmental, labor and national security violations associated with a stock being sold in the U.S.?" she asked.

An SEC spokesman, John Heine, said he could not comment specifically on PetroChina's prospectus, but he said foreign companies were held to the same standards as domestic ones when it came to disclosing "material" information about their practices.

According to Heine, this includes "all the information a reasonable investor needs to know to make an informed decision about an investment."

PetroChina's prospectus has not yet been declared effective, meaning that the company can not yet issue shares in the U.S. But the SEC's decision regarding PetroChina could set a precedent since this is the first time that such a controversial foreign company has sought to raise money on the U.S. markets.""")

  print keywords
  
if __name__ == "__main__":
  test()
