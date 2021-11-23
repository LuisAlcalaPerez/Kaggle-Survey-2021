import plotly.graph_objects as go

'''
-------------------------
        PIE CHART
-------------------------   
'''
def pie_chart(info ,question, values, labels, text):

    buttons = []

    fig = go.Figure()

    for k in range(len(labels)):
        label = labels[k]
        perc = 100.*values[k] / values.sum()

        fig.add_trace(go.Pie(
            values = values,
            labels = labels,
            pull = (labels == label) * 0.15,
            title = dict(text = '{0}<br>{1:1.2f}%'.format(question, perc) + text[k], font = dict(size = 18)),
            hoverinfo = 'label+percent'
        ))

        buttons.append({
            'label': label,
            'method': 'update',
            'args': [
                {'visible': [True if x == k else False for x in range(len(labels))]},
                {'title': label},
                {'selected': [True if label == info else False for x in labels]}
                ]
        })

    idx = labels.get_loc(info)
    fig.update_layout(
        margin = dict(t = 0, b = 0, l = 0, r = 0),
        updatemenus = [dict(type = 'dropdown', buttons = buttons, active = idx)]
    )
    fig.update_traces(textposition = 'inside', textinfo = 'label+percent')

    for k in range(len(labels)):
        fig.data[k].visible = False

    fig.data[idx].visible = True
    fig.show()
    

'''
-------------------------
        BAR CHART
-------------------------   
'''
def bar_chart_mean(info, sorted_mean, global_mean, text):
    
    buttons = []

    fig = go.Figure()

    sorted_labels = [item[0] for item in sorted_mean]
    sorted_values = [item[1] for item in sorted_mean]

    for k in range(len(sorted_labels)):
        label = sorted_labels[k]

        fig.add_trace(go.Bar(
            x = sorted_labels,
            y = sorted_values,
            marker = dict(color = ['#2471A3' if x == label else '#BBBBBB' for x in sorted_labels])
        ))

        buttons.append({
            'label': label,
            'method': 'update',
            'args': [
                {'visible': [True if x == k else False for x in range(len(sorted_labels))]},
                {'title': 'Participants from {0} are {1:1.2f} {2} {3} {4} tha the global average'.format(
                    sorted_labels[k], abs(global_mean - sorted_values[k]), text[0], text[1] if sorted_values[k] < global_mean else text[2], text[3])},
                {'selected': [True if label == info else False for x in sorted_labels]}
                ]
        })
    
    idx = sorted_labels.index(info)
    diff = sorted_values[idx] - global_mean

    fig.update_layout(
        updatemenus = [dict(type = 'dropdown', x = 0.99, y = 1.0, buttons = buttons, active= idx)],
        title = dict(text = 'Participants from {0} are {1:1.2f} {2} {3} {4} than the global average.'.format(
            info, abs(diff), text[0], text[1] if diff < 0 else text[2], text[3])),
        font = dict(size = 19),
        margin = dict(t = 50, b = 0, l = 0, r = 0),
        shapes = [dict(
            type = 'line',
            yref = 'y',
            y0 = global_mean,
            y1 = global_mean,
            xref = 'x',
            x0 = -1,
            x1 = len(sorted_labels)
        )]
    )

    fig.add_annotation(
        x = len(sorted_labels)*.90,
        y = global_mean + 1,
        text = 'Global Mean: {0:1.2f}'.format(global_mean),
        showarrow = False
    )

    for i in range(len(sorted_labels)):
        fig.data[i].visible = False
    
    fig.data[idx].visible = True
    fig.show()
