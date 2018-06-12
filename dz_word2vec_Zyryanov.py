
# coding: utf-8

# In[1]:


import sys
import gensim
model = gensim.models.KeyedVectors.load_word2vec_format('ruscorpora_upos_skipgram_300_5_2018.vec.gz', binary = False)


# In[2]:


center = 'вкус_NOUN'
#сначала ищем наиболее близкие слова к центру - это будут слова первого уровня. Цикл ищет все слова, для которых связь с центральным больше 0,5
last_similar = 1
topn = 5
while last_similar > 0.5:
    first_level = model.most_similar(positive=[center], topn = topn)
    last_similar = first_level[-1][1]
    topn += 1
print(len(first_level))


# In[37]:


second_level = {}
all_second_elems = []
#для каждого слова первого уровня подбираем наиболее близкие к нему слова - это второй уровень
#в цикле проверяем, чтобы во второй уровень добавлялись только уникальные слова
for word in first_level:
    full_element = model.most_similar(positive=[word[0]], topn = 15)
    pruned = []
    for el in full_element:
        if el[0] not in all_second_elems:
            all_second_elems.append(el[0])
            pruned.append(el)
    second_level[word] = pruned


# In[48]:


import  networkx  as nx
G = nx.Graph()
G.add_node(center, label = center)
#присоединяем к центру узлы первого уровня, 
#а затем к каждому узлу первого уровня присоединяем принадлежащие ему узлы второго уровня
#в этом цикле рисуем только связи между уровнями: центром и словами 1го уровня, словами 1го уровня и словами 2го уровня 
for el1 in first_level:
    G.add_node(el1[0], label = el1[0])
    if el1[1] > 0.5:
        G.add_edge(center, el1[0], weight = el1[1])
    for el2 in second_level[el1]:
        G.add_node(el2[0], label = el2[0])
        if el2[1] > 0.5:
            G.add_edge(el1[0], el2[0], weight = el2[1])
#теперь рисуем связь внутри второго уровня, если они больше 0,5:
for el1 in second_level:
    for el2 in second_level[el1]:
        for el22 in second_level[el1]:
            if el2[0] != el22[0]:
                dist = model.similarity(el2[0], el22[0])
                if dist > 0.5:
                    G.add_edge(el2[0], el22[0], weight = dist)
#связи внутри первого уровня:
for el1 in first_level:
    for el11 in first_level:
        if el1[0] != el11[0]:
                dist = model.similarity(el1[0], el11[0])
                if dist > 0.5:
                    G.add_edge(el1[0], el11[0], weight = dist)
            


# In[56]:


import matplotlib.pyplot as plt 
pos=nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_color='red', node_size=1)
nx.draw_networkx_edges(G, pos, edge_color='yellow')
nx.draw_networkx_labels(G, pos, font_size=2, font_family='Arial')
plt.axis('off')
plt.savefig('plot.png', dpi = 300)


# In[63]:


clust = nx.average_clustering(G)
print('Коэффициент кластеризации:', clust)
print('Главные вершины:')
centr_G = nx.degree_centrality(G)
i = 0
for nodeid in sorted(centr_G, key=centr_G.get, reverse=True):
    i += 1
    print(nodeid, round(centr_G[nodeid], 3))
    if i == 10:
        break

