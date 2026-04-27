import streamlit.components.v1 as components


def render_tradingview_chart(ticker):
    tradingview_html = f"""
    <div class="tradingview-widget-container">
      <div id="tradingview_chart"></div>

      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>

      <script type="text/javascript">
      new TradingView.widget({{
        "width": "100%",
        "height": 520,
        "symbol": "{ticker}",
        "interval": "D",
        "timezone": "Etc/UTC",
        "theme": "dark",
        "style": "1",
        "locale": "en",
        "toolbar_bg": "#0b0f19",
        "enable_publishing": false,
        "hide_top_toolbar": false,
        "save_image": false,
        "container_id": "tradingview_chart"
      }});
      </script>
    </div>
    """

    components.html(tradingview_html, height=540)