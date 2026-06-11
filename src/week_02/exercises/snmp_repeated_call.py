import snmp_testing_querying
import time
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.widgets import Slider

while True:
    snmp_testing_querying.main("10.250.38.43")
    df = pd.read_csv('snmp_data.csv') 
    ROWS_TO_SHOW = 30
    total_rows = len(df)

    fig, ax = plt.subplots(figsize=(max(14, len(df.columns) * 1.5), 15))
    plt.subplots_adjust(bottom=0.15) 

    def draw_table(start_row):
        ax.clear()
        ax.axis('off')
    
        # Slice the specific window of rows
        sliced_df = df.iloc[start_row : start_row + ROWS_TO_SHOW]
    
        # Render table grid
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

    # Initialize first view
    draw_table(0)

    # 4. Add interactive scrollbar slider
    ax_slider = plt.axes([0.4, 0.02, 0.2, 0.04])
    scrollbar = Slider(
        ax=ax_slider,
        label='Scroll Rows',
        valmin=0,
        valmax=total_rows - ROWS_TO_SHOW,
        valinit=0,
        valstep=25,
        valfmt='%0.0f'
    )

# 5. Update view when slider moves
    def update(val):
        draw_table(int(scrollbar.val))
        fig.canvas.draw_idle()

    scrollbar.on_changed(update)
    plt.show()

    time.sleep(10)