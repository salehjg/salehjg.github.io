import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

class ConferenceTimelinePlot:
    def __init__(self, data_json: dict, output_path: str):
        self.df = self._flatten_json(data_json)
        self.df["date"] = pd.to_datetime(self.df["date"], errors="coerce")
        self.df = self.df.dropna(subset=["date"])
        self.output_path = output_path
        self._build_and_save()

    def _flatten_json(self, data_json: dict) -> pd.DataFrame:
        records = []
        for conf, info in data_json.items():
            venue = info.get("venue", "")
            for key, value in info.items():
                if key.startswith("date_"):
                    if value in ("", "?", None):
                        continue
                    milestone_type = key.replace("date_", "").capitalize()
                    records.append({
                        "conf": conf,
                        "type": milestone_type,
                        "date": value,
                        "venue": venue
                    })
        return pd.DataFrame(records)

    def _build_and_save(self):
        timeline_bounds = self.df.groupby("conf").agg(
            start=("date", "min"),
            end=("date", "max"),
            venue=("venue", "first")
        ).reset_index()

        conf_order = timeline_bounds["conf"].tolist()
        conf_y = {name: i for i, name in enumerate(conf_order)}

        fig = go.Figure()

        # Add year background tints
        years = sorted(self.df["date"].dt.year.unique())
        colors = [
            "rgba(255, 223, 186, 0.1)",  # Pale orange
            "rgba(186, 225, 255, 0.1)",  # Pale blue
            "rgba(186, 255, 201, 0.1)",  # Pale green
            "rgba(255, 186, 255, 0.1)",  # Pale pink
            "rgba(255, 255, 186, 0.1)",  # Pale yellow
        ]

        # Map each year to a color cycling through the list
        year_color_map = {year: colors[i % len(colors)] for i, year in enumerate(years)}

        # Get min and max date in the data for full x-axis range
        min_date = self.df["date"].min()
        max_date = self.df["date"].max()

        for year in years:
            start = pd.Timestamp(f"{year}-01-01")
            end = pd.Timestamp(f"{year}-12-31")
            # Clamp to data range
            start = max(start, min_date)
            end = min(end, max_date)

            fig.add_shape(
                type="rect",
                xref="x",
                yref="paper",
                x0=start,
                x1=end,
                y0=0,
                y1=1,
                fillcolor=year_color_map[year],
                line_width=0,
                layer="below",
            )

        # Horizontal bars for each conference
        for _, row in timeline_bounds.iterrows():
            y = conf_y[row["conf"]]
            fig.add_trace(go.Scatter(
                x=[row["start"], row["end"]],
                y=[y, y],
                mode="lines",
                line=dict(width=10, color="lightgray"),
                showlegend=False,
                hovertemplate=f"{row['conf']}<br>Venue: {row['venue']}<br>%{{x|%Y-%m-%d}}"
            ))

        # Deadline markers
        for typ in self.df["type"].unique():
            df_type = self.df[self.df["type"] == typ]
            fig.add_trace(go.Scatter(
                x=df_type["date"],
                y=[conf_y[c] for c in df_type["conf"]],
                mode="markers",
                name=typ,
                marker=dict(size=12, symbol="circle"),
                hovertemplate=(
                    "Conference: %{y}<br>"
                    "Date: %{x|%Y-%m-%d}<br>"
                    f"Type: {typ}<br>"
                    "Venue: %{customdata[0]}"
                ),
                customdata=df_type[["venue"]].values
            ))

        fig.update_yaxes(
            tickvals=list(conf_y.values()),
            ticktext=list(conf_y.keys()),
            title="Conference"
        )
        fig.update_layout(
            title="Conference Deadlines Timeline",
            xaxis_title="Date",
            yaxis_title="Conference",
            height=300 + len(conf_y) * 40,
            xaxis=dict(type="date"),
            hovermode="closest",
        )

        fig.write_html(self.output_path)



if __name__ == "__main__":
    null = ""
    conference_data = {
        "NeurIPS 2025": {
            "date_abstract": "2025-05-11",
            "date_notification": null,
            "date_conf": "2025-12-02",
            "venue": "USA"
        },
        "ICLR 2025": {
            "date_abstract": "2024-09-27",
            "date_notification": "2025-01-22",
            "date_conf": "2025-04-24",
            "venue": "Singapore"
        },
        "ICLR 2026": {
            "date_abstract": null,
            "date_notification": null,
            "date_conf": "2026",
            "venue": "Lisbon"
        },
        "ICML 2025": {
            "date_abstract": "2025-01-23",
            "date_notification": null,
            "date_conf": "2025-07-13",
            "venue": "Canada"
        },
        "CVPR 2025": {
            "date_abstract": "2024-11-07",
            "date_notification": "2025-02-26",
            "date_conf": "2025-06-13",
            "venue": "USA"
        },
        "AAAI 2025": {
            "date_abstract": "2024-08-07",
            "date_notification": "2024-10-14",
            "date_conf": "2025-02-25",
            "venue": "USA"
        },
        "ECAI 2025": {
            "date_abstract": "2025-04-29",
            "date_notification": "2025-07-10",
            "date_conf": "2025-10-25",
            "venue": "Italy"
        },
        "ITDATA 2025": {
            "date_abstract": "2025-06-01",
            "date_notification": "2025-07-20",
            "date_conf": "2025-09-09",
            "venue": "Italy"
        },
        "ICPP 2025": {
            "date_abstract": "2025-05-01",
            "date_notification": "2025-06-10",
            "date_conf": "2025-09-08",
            "venue": "USA"
        },
        "IJCAI 2025": {
            "date_abstract": "2025-01-16",
            "date_notification": "2025-03-07",
            "date_conf": "2025-08-16",
            "venue": "Canada"
        },
        "AISTATS 2025": {
            "date_abstract": "2024-10-03",
            "date_notification": "2025-01-21",
            "date_conf": "2025-05-03",
            "venue": "Thailand"
        },
        "ICPR 2026": {
            "date_abstract": "2025-12-?",
            "date_notification": "2026-03-?",
            "date_conf": "2026-08-17",
            "venue": "France"
        },
        "ICANN 2025": {
            "date_abstract": "2025-02-15",
            "date_notification": "2025-05-25",
            "date_conf": "2025-09-09",
            "venue": "Lithuania"
        },
        "ECML 2025": {
            "date_abstract": "2025-03-07",
            "date_notification": "2025-10-13",
            "date_conf": "2025-09-15",
            "venue": "Portugal"
        },
        "BMVC 2025": {
            "date_abstract": "2025-05-09",
            "date_notification": "?",
            "date_conf": "2025-11-24",
            "venue": "UK"
        },
        "ACCAI 2025": {
            "date_abstract": "2025-02-25",
            "date_notification": "?",
            "date_conf": "2025-07-10",
            "venue": "Japan"
        },
        "ACML 2025": {
            "date_abstract": "2025-06-16",
            "date_notification": "2025-09-01",
            "date_conf": "2025-12-09",
            "venue": "Taiwan"
        },
        "ECCV 2026": {
            "date_abstract": "2026-03-06",
            "date_notification": "2026-05-?",
            "date_conf": "2026-09-08",
            "venue": "Sweden"
        },
        "ICCV 2025": {
            "date_abstract": "2025-03-03",
            "date_notification": "2025-06-26",
            "date_conf": "2025-10-19",
            "venue": "USA"
        },
        "EuroPAR 2025": {
            "date_abstract": "2025-02-24",
            "date_notification": "2025-04-30",
            "date_conf": "2025-08-25",
            "venue": "Germany"
        },
        "AICAS 2025": {
            "date_abstract": "2024-09-09",
            "date_notification": "2024-12-18",
            "date_conf": "2025-04-28",
            "venue": "France"
        },
        "ISPDC 2025": {
            "date_abstract": "2025-04-18",
            "date_notification": "2025-05-30",
            "date_conf": "2025-07-08",
            "venue": "France"
        }
    }

    plotter = ConferenceTimelinePlot(conference_data, "timeline.html")

