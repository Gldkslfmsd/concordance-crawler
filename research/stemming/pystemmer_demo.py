import Stemmer

stemmer = Stemmer.Stemmer('english')

from samples import test
test(stemmer.stemWord)
