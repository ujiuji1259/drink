import MeCab
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pickle

def space_split(s):
    return s.split(' ')


class Episodes(object):
    def __init__(self, all_episodes, model):
        self.parser = MeCab.Tagger('-Owakati')
        self.all_episodes = np.array(all_episodes)
        self.all_tokens = [self.parser.parse(s) for s in all_episodes]

        self.model = model
        self.all_vec = self.model.transform(self.all_tokens)

    def find_similar_episode(self, sents, k=1):
        tokens = [self.parser.parse(s) for s in sents]
        vecs = self.model.transform(tokens)

        sims = cosine_similarity(vecs, self.all_vec)
        rank = np.argsort(sims, axis=1)[:, ::-1]
        rank = rank[:, :k]

        episodes = [self.all_episodes[r].tolist() if len(s) >= 10 else [''] for r, s in zip(rank, sents)]

        return episodes





if __name__ == "__main__":
    with open('all_episode.txt', 'r') as f:
        all_episode = []
        for line in f:
            line = line.rstrip()
            if not line:
                continue

            all_episode.append(line)

    with open('similar_episode.txt', 'r') as f:
        similar_episode = []
        for line in f:
            line = line.rstrip()
            if not line:
                continue

            similar_episode.append(line)

    """
    with open('episode_tfidf.pkl', 'rb') as f:
        model = pickle.load(f)

    finder = Episodes(similar_episode, model)
    finder.find_similar_episode(['禁酒辛すぎ'], 10)

    """
    parser = MeCab.Tagger('-Owakati')
    all_episode = [parser.parse(s) for s in all_episode]
    similar_episode = [parser.parse(s) for s in similar_episode]

    model = TfidfVectorizer()
    model.fit(all_episode)

    all_vec = model.transform(all_episode)
    sim_vec = model.transform(similar_episode)
    sims = cosine_similarity(sim_vec, all_vec)
    rank = np.argsort(sims, axis=1)[:, ::-1]
    print(model.vocabulary_)

    with open('episode_tfidf.pkl', 'wb') as f:
        pickle.dump(model, f)

