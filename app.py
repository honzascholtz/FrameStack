from flask import Flask, render_template, request
import os
import tempfile
import base64
import io
import matplotlib
matplotlib.use('Agg')  # Required for headless server environments
import matplotlib.pyplot as plt

from FrameStack import FrameStack, plot_comparison
import Graph_setup as gph

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    image_data = None
    geo_data_list = []
    error = None
    
    # Default geometry to show in the text area
    default_geo = """Head Angle\t73.0
Seat Angle\t73.5
Stack\t590
Reach\t385
Head Tube\t140
Seat Tube C-C\t530
Top Tube (effective)\t560
Chainstay\t415
BB Drop\t70
Front Centre\t595
Wheelbase\t1010
Fork Rake / Offset\t50
Seat height\t720
Spacers\t20
Stem length\t100
Stem Angle\t6.0
Bar width\t420"""

    geo_texts = request.form.getlist('geo_text')
    bike_names = request.form.getlist('bike_name')
    column_indices_raw = request.form.getlist('column_index')
    
    spacers_list = request.form.getlist('spacers')
    stem_lengths = request.form.getlist('stem_length')
    stem_angles = request.form.getlist('stem_angle')
    bar_widths = request.form.getlist('bar_width')
    
    if request.method == 'GET' or not geo_texts:
        geo_texts = [default_geo]
        bike_names = ["My Bike"]
        column_indices_raw = ["1"]
        spacers_list = ["20"]
        stem_lengths = ["100"]
        stem_angles = ["6.0"]
        bar_widths = ["420"]

    # Pad lists to ensure zip doesn't truncate if some fields are missing
    for lst in [spacers_list, stem_lengths, stem_angles, bar_widths]:
        while len(lst) < len(geo_texts):
            lst.append("")

    # Convert 1-based UI indices to 0-based backend indices
    column_indices = []
    for c in column_indices_raw:
        try:
            column_indices.append(max(0, int(c) - 1))
        except ValueError:
            column_indices.append(0)

    # Combine for the template (keep 1-based for the UI template)
    bikes_input = list(zip(bike_names, geo_texts, column_indices_raw, spacers_list, stem_lengths, stem_angles, bar_widths))
    valid_names = []
    valid_col_indices = []

    if request.method == 'POST':
        valid_texts = []
        valid_spacers = []
        valid_sl = []
        valid_sa = []
        valid_bw = []
        for name, text, col_idx, sp, sl, sa, bw in zip(bike_names, geo_texts, column_indices, spacers_list, stem_lengths, stem_angles, bar_widths):
            if text.strip():
                # Append cockpit values if provided via UI overrides
                if sp.strip(): text += f"\nSpacers\t{sp.strip()}"
                if sl.strip(): text += f"\nStem length\t{sl.strip()}"
                if sa.strip(): text += f"\nStem Angle\t{sa.strip()}"
                if bw.strip(): text += f"\nBar width\t{bw.strip()}"
                
                valid_texts.append(text)
                valid_names.append(name.strip() or f"Bike {len(valid_texts)}")
                valid_col_indices.append(col_idx)
                valid_spacers.append(sp.strip())
                valid_sl.append(sl.strip())
                valid_sa.append(sa.strip())
                valid_bw.append(bw.strip())
        
        # Update template inputs to only show the valid submitted ones
        if valid_texts:
            bikes_input = list(zip(valid_names, valid_texts, [str(c+1) for c in valid_col_indices], valid_spacers, valid_sl, valid_sa, valid_bw))
        else:
            bikes_input = [("My Bike", default_geo, "1", "20", "100", "6.0", "420")]
            
        if valid_texts:
            paths = []
            try:
                # 1. Save all input texts to temporary files
                for text in valid_texts:
                    fd, path = tempfile.mkstemp(suffix='.txt')
                    with os.fdopen(fd, 'w') as f:
                        f.write(text)
                    paths.append(path)
                
                # 2. Parse geometry for display
                for path, col_idx in zip(paths, valid_col_indices):
                    bike = FrameStack(path, column_index=col_idx)
                    geo_data_list.append(bike.geo)
                
                # 3. Create matplotlib figure
                if len(paths) == 1:
                    fig, ax = plt.subplots(figsize=(12, 8))
                    bike = FrameStack(paths[0], column_index=valid_col_indices[0])
                    bike.plot_bike(fig, ax)
                    ax.set_title(valid_names[0], fontsize=16, fontweight='bold', pad=16)
                else:
                    fig, ax = plot_comparison(paths, names=valid_names, column_indices=valid_col_indices)
                
                # 4. Save figure to a base64 string buffer
                buf = io.BytesIO()
                fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
                plt.close(fig)
                
                buf.seek(0)
                image_data = base64.b64encode(buf.getvalue()).decode('utf-8')
                
            except Exception as e:
                error = f"Error processing geometry: {str(e)}"
            finally:
                for path in paths:
                    if os.path.exists(path):
                        os.remove(path)

    # Zip names and parsed data for the tables
    parsed_bikes = list(zip(valid_names, geo_data_list)) if valid_names else []

    return render_template('index.html', 
                           bikes_input=bikes_input, 
                           image_data=image_data, 
                           parsed_bikes=parsed_bikes, 
                           error=error)

if __name__ == '__main__':
    app.run(debug=True, port=5000)