import plotly.graph_objects as go

import networkx as nx
import matplotlib.pyplot as plt

topics = ['Feeding', 'Mood', "Alzheimer's", 'Suicide', 'Locomotion', 'Memory', 'Analgesic', 'Obesity', 'Psychedelics', 'Pain',
          'Anxiolytic', 'Nausea', 'Emesis', 'Stress', 'Anxiety', 'Cognition', 'Vasoconstriction', 'Compulsivity', 'Psychosis',
          'Anxiogenic', 'Addiction', 'Gastrointestinal', 'Impulsivity', 'Sex', 'Schizophrenia', 'Sleep', 'Aggression', 'Learning',
          'Appetite', 'Dementia', 'Depression', 'Cardiovascular']

receptors = ['5-HT1A',
            '5-HT1B',
            '5-HT1D',
            '5-HT1E',
            '5-HT1F',
            '5-HT2A',
            '5-HT2B',
            '5-HT2C',
            '5-HT3',
            '5-HT4',
            '5-HT5A',
            '5-HT6',
            '5-HT7']

receptor_to_topic = {
    '5-HT1A': ['Depression', 'Anxiolytic', 'Anxiety', 'Stress', 'Sex', 'Suicide'],
    '5-HT1B': ['Aggression', 'Feeding', 'Vasoconstriction', 'Pain', 'Impulsivity'],
    '5-HT1D': ['Pain', 'Vasoconstriction'],
    '5-HT1E': ['Pain', 'Anxiety', 'Schizophrenia', 'Depression'],
    '5-HT1F': ['Pain', 'Sleep'],
    '5-HT2A': ['Schizophrenia', 'Psychedelics', 'Psychosis', 'Mood', 'Cognition', 'Impulsivity', 'Compulsivity'],
    '5-HT2B': ['Cardiovascular', 'Obesity', 'Anxiogenic', 'Anxiolytic', 'Vasoconstriction'],
    '5-HT2C': ['Feeding', 'Appetite', 'Obesity', 'Locomotion', 'Anxiety', 'Anxiogenic', 'Addiction', 'Compulsivity'],
    '5-HT3': ['Emesis', 'Nausea', 'Pain', 'Analgesic', 'Gastrointestinal'],
    '5-HT4': ['Memory', 'Alzheimer\'s', 'Cognition', 'Gastrointestinal', 'Learning', 'Pain'],
    '5-HT5A': ['Learning'],
    '5-HT6': ['Cognition', 'Memory', 'Learning', 'Alzheimer\'s', 'Schizophrenia', 'Dementia', 'Obesity', 'Psychosis'],
    '5-HT7': ['Memory', 'Sleep', 'Cognition', 'Learning', 'Mood', 'Pain', 'Schizophrenia', 'Dementia', 'Cardiovascular', 'Depression']
}

topic_to_receptor = {}

for k,v in receptor_to_topic.iteritems():
    for topic in v:
        if topic in topic_to_receptor:
            topic_to_receptor[topic].append(k)
        else:
            topic_to_receptor[topic] = [k]





def plot_graph(G, name):
    pos = nx.spring_layout(G)

    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append(adjacencies[0])

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='<br>{}'.format(name),
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        annotations=[dict(
                            text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002)],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    fig.show()


def make_plot(type='Topic', cutoff=1):
    G = nx.Graph()
    if type == 'Topic':
        nodes = topics
        edges = topic_to_receptor
    elif type == 'Receptor':
        nodes = receptors
        edges = receptor_to_topic
    else:
        raise Exception('unrecognized type {}'.format(topic))

    for n in nodes:
        G.add_node(n)

    for n1 in edges:
            for n2 in edges:
                if n1 != n2:
                    l1 = edges[n1]
                    l2 = edges[n2]

                    intersection = [l for l in l1 if l in l2]
                    if len(intersection) >= cutoff:
                        G.add_weighted_edges_from([(n1, n2, len(intersection))])

    plot_graph(G, '{} co-occurrences'.format(type))


if __name__ == '__main__':
    make_plot('Topic', cutoff=2)
    make_plot('Receptor', cutoff=2)