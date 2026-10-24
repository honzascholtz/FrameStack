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
    
    if request.method == 'GET' or not geo_texts:
        geo_texts = [default_geo]
        bike_names = ["My Bike"]

    # Combine for the template
    bikes_input = list(zip(bike_names, geo_texts))
    valid_names = []

    if request.method == 'POST':
        valid_texts = []
        for name, text in bikes_input:
            if text.strip():
                valid_texts.append(text)
                valid_names.append(name.strip() or f"Bike {len(valid_texts)}")
        
        # Update template inputs to only show the valid submitted ones
        if valid_texts:
            bikes_input = list(zip(valid_names, valid_texts))
        else:
            bikes_input = [("My Bike", default_geo)]
            
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
                for path in paths:
                    bike = FrameStack(path)
                    geo_data_list.append(bike.geo)
                
                # 3. Create matplotlib figure
                if len(paths) == 1:
                    fig, ax = plt.subplots(figsize=(12, 8))
                    bike = FrameStack(paths[0])
                    bike.plot_bike(fig, ax)
                    ax.set_title(valid_names[0], fontsize=16, fontweight='bold', pad=16)
                else:
                    fig, ax = plot_comparison(paths, names=valid_names)
                
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