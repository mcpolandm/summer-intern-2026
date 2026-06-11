import snmp_testing_querying
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.widgets import Slider

ROWS_TO_SHOW = 30

plt.ion()

snmp_testing_querying.main("10.250.38.43")
df = pd.read_csv('snmp_data.csv')

fig, ax = plt.subplots(figsize=(max(14, len(df.columns) * 1.5), 15))
plt.subplots_adjust(bottom=0.15)

def draw_table(start_row):
    ax.clear()
    ax.axis('off')
    sliced_df = df.iloc[start_row : start_row + ROWS_TO_SHOW]
    table = ax.table(
        cellText=sliced_df.values,
        colLabels=df.columns,
        cellLoc='center',
        loc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.auto_set_column_width(col=list(range(len(df.columns))))
    table.scale(1.0, 1.8)

draw_table(0)

ax_slider = plt.axes([0.4, 0.02, 0.2, 0.04])
scrollbar = Slider(
    ax=ax_slider,
    label='Scroll Rows',
    valmin=0,
    valmax=max(1, len(df) - ROWS_TO_SHOW),
    valinit=0,
    valstep=25,
    valfmt='%0.0f'
)

def update(val):
    draw_table(int(scrollbar.val))
    fig.canvas.draw_idle()

scrollbar.on_changed(update)
plt.show()

while True:
    plt.pause(10)
    snmp_testing_querying.main("10.250.38.43")
    df = pd.read_csv('snmp_data.csv')
    scrollbar.valmax = max(1, len(df) - ROWS_TO_SHOW)
    scrollbar.ax.set_xlim(0, scrollbar.valmax)
    draw_table(int(scrollbar.val))
    fig.canvas.draw_idle()
