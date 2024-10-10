import plotly.graph_objects as go
from plotly.subplots import make_subplots
import polars as pl
from typing import List, Optional
from RNApysoforms.utils import check_df  # Ensure this is correctly imported
from RNApysoforms import set_axis

def make_plot(
    traces: List[go.Trace],
    y: str = "transcript_id",
    subplot_titles: List[str] = ["Transcript Structure"],
    horizontal_spacing: float = 0.02,
    vertical_spacing: float = 0.02,
    showlegend: bool = True,
    height: int = 800,
    width: int = 1800,
    template: str = "plotly_white",
    boxgroupgap=0.8,
    boxgap=0.2,
    vert_grid_transcript_structure_plot=True,
    horz_grid_transcript_structure_plot=True,
    vert_grid_expression_plot=True,
    horz_grid_expression_plot=True,
) -> go.Figure:
    """
    Create a Plotly figure with multiple aligned subplots.
    
    [Docstring remains unchanged for brevity]
    """
    y_dict = traces[-1]

    full_trace_list = traces[:-1]

    print(len(full_trace_list))


    # Initialize the subplot figure with shared y-axes
    fig = make_subplots(
        rows=1,
        cols=len(full_trace_list),
        subplot_titles=subplot_titles,
        horizontal_spacing=horizontal_spacing,
        vertical_spacing=vertical_spacing,
        shared_yaxes=True,  # Share y-axes across all subplots
    )

    fig.update_layout(
        template=template
    )

    transcript_traces = []
    expression_traces = []
    transcript_indexes = []
    expression_indexes = []

    index=1
    for trace in full_trace_list:
        
        if hasattr(trace[0], 'type'):
            expression_traces.extend(trace)
            expression_indexes.append(index)
        elif isinstance(trace[0], dict):
            transcript_traces.append(trace)
            transcript_indexes.append(index)

        index=index+1

    # Add all traces to their respective subplots
    for i, subplot_traces in enumerate(full_trace_list, start=1):

        fig.add_traces(
            subplot_traces,
            rows=[1] * len(subplot_traces),
            cols=[i] * len(subplot_traces)
        )

    for i in transcript_indexes:
        # Customize x-axes
        # First subplot (Transcript Structure)
        fig.update_xaxes(
            showticklabels=False,
            title="",
            row=1,
            col=i,
            showgrid=horz_grid_transcript_structure_plot
        )

        # Customize the shared y-axis (only for the first subplot)
        fig.update_yaxes(
            tickvals=list(y_dict.values()),
            ticktext=list(y_dict.keys()),
            tickfont=dict(size=10, family='DejaVu Sans', color='black'),
            title="",  # Optional
            row=1,
            col=i,
            showgrid=vert_grid_transcript_structure_plot
        )


    
    for i in expression_indexes:
        fig.update_xaxes(
            showticklabels=True,  # Show x-axis labels for expression plots
            title=f"",  # Customize as needed
            row=1,
            col=i,
            showgrid=horz_grid_expression_plot
        )
        # Hide y-axis labels for additional subplots
        fig.update_yaxes(
            tickvals=list(y_dict.values()),
            ticktext=list(y_dict.keys()),
            showticklabels=False,
            ticks='',
            row=1,
            col=i,
            range=[-0.8, (len(y_dict) - 0.2)],
            showgrid=vert_grid_expression_plot
        )

    # Customize the shared y-axis (only for the first subplot)
    fig.update_yaxes(
        ticks="outside",
        tickvals=list(y_dict.values()),
        ticktext=list(y_dict.keys()),
        tickfont=dict(size=10, family='DejaVu Sans', color='black'),
        title="",  # Optional
        row=1,
        col=1)


    # Update overall layout
    fig.update_layout(
        title_text="",
        showlegend=showlegend,
        height=height,
        width=width,
        hoverlabel=dict(font=dict(size=12)),
        margin=dict(l=100, r=50, t=100, b=50),  # Adjust margins as needed
        boxmode='group',
        legend_tracegroupgap=7,
        boxgroupgap=boxgroupgap, 
        boxgap=boxgap,
        violinmode='group',
        violingroupgap=boxgroupgap,
        violingap=boxgap,
        yaxis=dict(range=[-0.8, ( len(y_dict) - 0.2)])
    )

    return fig
