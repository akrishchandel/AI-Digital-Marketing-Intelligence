from flask import Flask, render_template, request, Response
import pandas as pd
import json
import joblib

app = Flask(__name__)


# ==========================================
# LOAD DATA AND ML MODEL
# ==========================================

df = pd.read_csv("data/analyzed_campaigns.csv")

model = joblib.load("model/conversion_model.pkl")


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/", methods=["GET", "POST"])
def home():

    # ======================================
    # OVERALL METRICS
    # ======================================

    total_spend = df["spend"].sum()

    total_revenue = df["revenue"].sum()

    total_clicks = df["clicks"].sum()

    total_conversions = df["conversions"].sum()

    total_impressions = df["impressions"].sum()

    ctr = (
        total_clicks /
        total_impressions
    ) * 100

    conversion_rate = (
        total_conversions /
        total_clicks
    ) * 100

    roas = (
        total_revenue /
        total_spend
    )


    # ======================================
    # CAMPAIGN PERFORMANCE SUMMARY
    # ======================================

    campaign_summary = df.groupby(
        ["campaign", "platform"]
    ).agg({

        "impressions": "sum",

        "clicks": "sum",

        "conversions": "sum",

        "spend": "sum",

        "revenue": "sum"

    }).reset_index()


    # ======================================
    # CAMPAIGN METRICS
    # ======================================

    campaign_summary["CTR"] = (
        campaign_summary["clicks"] /
        campaign_summary["impressions"]
    ) * 100

    campaign_summary["Conversion_Rate"] = (
        campaign_summary["conversions"] /
        campaign_summary["clicks"]
    ) * 100

    campaign_summary["ROAS"] = (
        campaign_summary["revenue"] /
        campaign_summary["spend"]
    )

    campaign_summary["ROI"] = (
        (
            campaign_summary["revenue"] -
            campaign_summary["spend"]
        )
        /
        campaign_summary["spend"]
    ) * 100


    # ======================================
    # CAMPAIGN PERFORMANCE RATING
    # ======================================

    def get_campaign_rating(roas_value):

        if roas_value >= 2:

            return "Excellent"

        elif roas_value >= 1:

            return "Good"

        elif roas_value >= 0.5:

            return "Needs Improvement"

        else:

            return "Poor"


    campaign_summary["Rating"] = (
        campaign_summary["ROAS"]
        .apply(get_campaign_rating)
    )

    # ======================================
    # RATING SUMMARY
    # ======================================

    excellent_count = (
        campaign_summary["Rating"] == "Excellent"
    ).sum()

    good_count = (
        campaign_summary["Rating"] == "Good"
    ).sum()

    improvement_count = (
        campaign_summary["Rating"] == "Needs Improvement"
    ).sum()

    poor_count = (
        campaign_summary["Rating"] == "Poor"
    ).sum()

    # ======================================
    # CAMPAIGN RECOMMENDATION
    # ======================================

    def get_campaign_recommendation(row):

        if row["ROAS"] >= 2:

            return (
                "Strong performance. "
                "Consider increasing budget gradually."
            )

        elif row["ROAS"] >= 1:

            return (
                "Good performance. "
                "Continue the campaign and optimize creatives."
            )

        elif row["ROAS"] >= 0.5:

            return (
                "Performance needs improvement. "
                "Review targeting and ad creatives."
            )

        else:

            return (
                "Poor performance. "
                "Consider reducing spend and reviewing the campaign."
            )


    campaign_summary["Recommendation"] = (
        campaign_summary.apply(
            get_campaign_recommendation,
            axis=1
        )
    )


    # ======================================
    # ROUND NUMERICAL VALUES
    # ======================================

    campaign_summary[
        [
            "CTR",
            "Conversion_Rate",
            "ROAS",
            "ROI"
        ]
    ] = campaign_summary[
        [
            "CTR",
            "Conversion_Rate",
            "ROAS",
            "ROI"
        ]
    ].round(2)


    # ======================================
    # BEST CAMPAIGN
    # ======================================

    best_campaign = campaign_summary.loc[
        campaign_summary["ROAS"].idxmax()
    ]

    best_campaign_name = (
        best_campaign["campaign"]
    )

    best_campaign_roas = (
        best_campaign["ROAS"]
    )


    # ======================================
    # WORST CAMPAIGN
    # ======================================

    worst_campaign = campaign_summary.loc[
        campaign_summary["ROAS"].idxmin()
    ]

    worst_campaign_name = (
        worst_campaign["campaign"]
    )

    worst_campaign_roas = (
        worst_campaign["ROAS"]
    )


    # ======================================
    # PLATFORM ANALYSIS
    # ======================================

    platform_analysis = df.groupby(
        "platform"
    ).agg({

        "spend": "sum",

        "revenue": "sum",

        "clicks": "sum",

        "conversions": "sum",

        "impressions": "sum"

    }).reset_index()


    platform_analysis["CTR"] = (
        platform_analysis["clicks"] /
        platform_analysis["impressions"]
    ) * 100


    platform_analysis["Conversion_Rate"] = (
        platform_analysis["conversions"] /
        platform_analysis["clicks"]
    ) * 100


    platform_analysis["ROAS"] = (
        platform_analysis["revenue"] /
        platform_analysis["spend"]
    )


    platform_analysis["ROI"] = (
        (
            platform_analysis["revenue"] -
            platform_analysis["spend"]
        )
        /
        platform_analysis["spend"]
    ) * 100


    platform_analysis = platform_analysis.round(2)


    # ======================================
    # BEST PLATFORM
    # ======================================

    best_platform = platform_analysis.loc[
        platform_analysis["ROAS"].idxmax()
    ]

    best_platform_name = (
        best_platform["platform"]
    )

    best_platform_roas = (
        best_platform["ROAS"]
    )


    # ======================================
    # OVERALL RECOMMENDATION
    # ======================================

    if best_platform_roas >= 2:

        recommendation = (
            f"{best_platform_name} is performing strongly "
            f"with a ROAS of {best_platform_roas:.2f}x. "
            "Consider testing a higher budget allocation "
            "while monitoring performance."
        )

    elif roas < 1:

        recommendation = (
            "Overall ROAS is below 1x. "
            "Review campaign targeting, ad creatives, "
            "and landing pages before increasing the budget."
        )

    elif ctr < 2:

        recommendation = (
            "Overall CTR is relatively low. "
            "Consider improving ad creatives and audience targeting."
        )

    else:

        recommendation = (
            "Campaign performance is relatively stable. "
            "Continue monitoring CTR, conversion rate, and ROAS "
            "to identify optimization opportunities."
        )


    # ======================================
    # CHART DATA
    # ======================================

    platform_names = (
        platform_analysis["platform"]
        .tolist()
    )


    platform_revenue = (
        platform_analysis["revenue"]
        .tolist()
    )


    campaign_chart_data = (
        campaign_summary
        .groupby("campaign")["ROAS"]
        .mean()
    )


    campaign_names = (
        campaign_chart_data
        .index
        .tolist()
    )


    campaign_roas = (
        campaign_chart_data
        .values
        .tolist()
    )


    # ======================================
    # FILTER LISTS
    # ======================================

    platform_list = sorted(
        campaign_summary["platform"]
        .unique()
        .tolist()
    )


    campaign_list = sorted(
        campaign_summary["campaign"]
        .unique()
        .tolist()
    )


    # ======================================
    # CAMPAIGN TABLE
    # ======================================

    campaign_table = campaign_summary[
        [
            "campaign",
            "platform",
            "CTR",
            "Conversion_Rate",
            "ROAS",
            "ROI",
            "Rating",
            "Recommendation"
        ]
    ].to_dict(
        orient="records"
    )


    # ======================================
    # ML PREDICTION
    # ======================================

    prediction = None

    error = None


    if request.method == "POST":

        try:

            impressions = float(
                request.form["impressions"]
            )

            clicks = float(
                request.form["clicks"]
            )

            spend = float(
                request.form["spend"]
            )


            # ------------------------------
            # VALIDATION
            # ------------------------------

            if impressions <= 0:

                raise ValueError(
                    "Impressions must be greater than 0."
                )


            if clicks < 0:

                raise ValueError(
                    "Clicks cannot be negative."
                )


            if clicks > impressions:

                raise ValueError(
                    "Clicks cannot be greater than impressions."
                )


            if spend < 0:

                raise ValueError(
                    "Ad spend cannot be negative."
                )


            # ------------------------------
            # CREATE INPUT DATA
            # ------------------------------

            input_data = pd.DataFrame({

                "impressions": [impressions],

                "clicks": [clicks],

                "spend": [spend]

            })


            # ------------------------------
            # ML PREDICTION
            # ------------------------------

            prediction = model.predict(
                input_data
            )[0]


            prediction = max(
                0,
                round(prediction)
            )


        except ValueError as e:

            prediction = None

            error = str(e)


    # ======================================
    # SEND DATA TO HTML
    # ======================================

    return render_template(

        "index.html",

        total_spend=f"{total_spend:,.2f}",

        total_revenue=f"{total_revenue:,.2f}",

        total_clicks=f"{total_clicks:,}",

        total_conversions=f"{total_conversions:,}",

        ctr=f"{ctr:.2f}",

        conversion_rate=f"{conversion_rate:.2f}",

        roas=f"{roas:.2f}",


        best_campaign_name=best_campaign_name,

        best_campaign_roas=(
            f"{best_campaign_roas:.2f}"
        ),


        worst_campaign_name=worst_campaign_name,

        worst_campaign_roas=(
            f"{worst_campaign_roas:.2f}"
        ),


        best_platform_name=best_platform_name,

        best_platform_roas=(
            f"{best_platform_roas:.2f}"
        ),


        recommendation=recommendation,


        platform_names=json.dumps(
            platform_names
        ),


        platform_revenue=json.dumps(
            platform_revenue
        ),


        campaign_names=json.dumps(
            campaign_names
        ),


        campaign_roas=json.dumps(
            campaign_roas
        ),


        prediction=prediction,

        error=error,


        campaign_table=campaign_table,

        platform_list=platform_list,

        campaign_list=campaign_list,

        excellent_count=excellent_count,

        good_count=good_count,

        improvement_count=improvement_count,

        poor_count=poor_count,
    )

# ==========================================
# DOWNLOAD CAMPAIGN REPORT
# ==========================================

@app.route("/download-report")
def download_report():

    report_df = pd.read_csv(
        "data/analyzed_campaigns.csv"
    )


    report = report_df.groupby(
        ["campaign", "platform"]
    ).agg({

        "impressions": "sum",

        "clicks": "sum",

        "conversions": "sum",

        "spend": "sum",

        "revenue": "sum"

    }).reset_index()


    report["CTR"] = (
        report["clicks"] /
        report["impressions"]
    ) * 100


    report["Conversion_Rate"] = (
        report["conversions"] /
        report["clicks"]
    ) * 100


    report["ROAS"] = (
        report["revenue"] /
        report["spend"]
    )


    report["ROI"] = (
        (
            report["revenue"] -
            report["spend"]
        )
        /
        report["spend"]
    ) * 100


    def rating(roas):

        if roas >= 2:
            return "Excellent"

        elif roas >= 1:
            return "Good"

        elif roas >= 0.5:
            return "Needs Improvement"

        else:
            return "Poor"


    report["Rating"] = (
        report["ROAS"]
        .apply(rating)
    )


    report["Recommendation"] = (
        report["ROAS"]
        .apply(
            lambda x:
            "Strong performance. Consider increasing budget gradually."
            if x >= 2
            else
            "Good performance. Continue the campaign and optimize creatives."
            if x >= 1
            else
            "Performance needs improvement. Review targeting and ad creatives."
            if x >= 0.5
            else
            "Poor performance. Consider reducing spend and reviewing the campaign."
        )
    )


    report = report.round(2)


    report = report[
        [
            "campaign",
            "platform",
            "CTR",
            "Conversion_Rate",
            "ROAS",
            "ROI",
            "Rating",
            "Recommendation"
        ]
    ]


    csv_data = report.to_csv(
        index=False
    )


    return Response(

        csv_data,

        mimetype="text/csv",

        headers={
            "Content-Disposition":
            "attachment; filename=campaign_report.csv"
        }

    )
# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(debug=True)