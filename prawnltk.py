import praw
import operator
import nltk

r = praw.Reddit('NLTK comment parser /u/USERNAME')
r.login('USERNAME', 'PASSWORD')
subreddit = r.get_subreddit('askreddit')

# Download these libraries for the NLTK if you haven't already
#nltk.download('punkt')
#nltk.download('words')
#nltk.download('stopwords')

stop_word_list = """.,--,\'s,?,),(,:,\',\'re,",-,},{,!,...,\'\',\'ve,n\'t,%,``,#,],[,&,;,\'m,=,\'ll""".split(',')
stop_word_list = stop_word_list.extend([u'—', ','])
stop_words = nltk.corpus.stopwords.words('english') + stop_word_list

for submission in subreddit.get_hot(limit=2):
    print submission.title
    print "==" * 30
    post = r.get_submission(submission_id=submission.id)
    post.replace_more_comments(limit=None, threshold=0)
    flat_comments = praw.helpers.flatten_tree(post.comments)
    all_comments = ""
    for comment in flat_comments:
        all_comments += comment.body
    sentences = nltk.tokenize.sent_tokenize(all_comments)
    
    words = [w.lower() for sentence in sentences for w in
         nltk.tokenize.word_tokenize(sentence)]

    fdist = nltk.FreqDist(words)

    # Basic stats

    num_words = sum([i[1] for i in fdist.items()])
    num_unique_words = len(fdist.keys())

    # Hapaxes are words that appear only once

    num_hapaxes = len(fdist.hapaxes())

    top_10_words_sans_stop_words = [w for w in fdist.items() if w[0]
                                    not in stop_words][:10]

    print '\tNum Sentences:'.ljust(25), len(sentences)
    print '\tNum Words:'.ljust(25), num_words
    print '\tNum Unique Words:'.ljust(25), num_unique_words
    print '\tNum Hapaxes:'.ljust(25), num_hapaxes
    print '\tTop 10 Most Frequent Words (sans stop words):\n\t\t', \
            '\n\t\t'.join(['%s (%s)'
            % (w[0], w[1]) for w in top_10_words_sans_stop_words])
    print "\n"
