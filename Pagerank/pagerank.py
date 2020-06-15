import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    #Gets starting probabilities to every site and makes a list of the final probability.
    startingProb = (1-damping_factor) / len(corpus)
    probs = {}

    #Assigns the starting probability to each site.
    for site in corpus:
        probs[site] = startingProb

    #If the page we are on has no links on it, it will distribute the remaining probability to all sites equally.
    if corpus[page] is None:
        for site in corpus:
            probs[site] += damping_factor / len(corpus)

    #Distributes remaining probability equally to all pages that are linked on this site.
    else:
        for site in corpus[page]:
            probs[site] += damping_factor / len(corpus[page])

    return probs

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    #Samples will hold all samples and ranks will hold final ranks of pages.
    samples = []
    ranks = {}

    #A random site will be chosen and added as the first sample
    sample = random.choice(list(corpus))
    samples.append(sample)

    #For the other samples, they will be randomly chosen with correct weightings.
    for i in range(n-1):
        siteprobs = transition_model(corpus, sample, damping_factor)

        #To assign a range of probability to each site, the first site will be from 0-firstsitechance, second will be firstsitechance-secondsitechance, etc.
        randomnum = random.random()
        currentcap = 0
        for site in siteprobs:
            currentcap += siteprobs[site]
            if randomnum < currentcap:
                sample = site
                samples.append(sample)
                break

    #The probability of each site that was a sample will be calculated
    for site in corpus:
        ranks[site] = samples.count(site)/n

    return ranks



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    #This will hold all ranks.
    ranks = {}

    #Assigns initial probability to all sites (should be equal).
    for site in corpus:
        ranks[site] = 1 / len(corpus)

    #Keeps track of the maximum change
    maxchange = 1/len(corpus)

    #Keeps adjsuting values until the maximum change that occurs is less than 0.001.
    while maxchange > 0.001:
        for site in corpus:
            rest = 0
            maxchange = 0

            #rest variable is what I used to do the second part of the equation in the background part of the project desc.
            for linkedsite in corpus:
                if site in corpus[linkedsite]:
                    rest += ranks[linkedsite]/len(corpus[linkedsite])
            rest *= damping_factor

            #The new score is adjusted based on the equation.
            newscore = (1-damping_factor)/len(corpus) + rest
            change = abs(newscore - ranks[site])
            if change > maxchange:
                maxchange = abs(newscore - ranks[site])
            ranks[site] = newscore

    return ranks

if __name__ == "__main__":
    main()
