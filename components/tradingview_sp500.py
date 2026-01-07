import streamlit as st
import streamlit.components.v1 as components


def render_tradingview_sp500():
    st.subheader("📈 S&P 500 (TradingView)")

    tradingview_html = """
    <div class="tradingview-widget-container">
      <div id="tradingview_spx"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
new TradingView.widget({
  "width": "100%",
  "height": 500,
  "symbol": "AMEX:SPY",
  "interval": "M",
  "timezone": "Etc/UTC",
  "theme": "light",
  "style": "1",
  "locale": "fr",
  "allow_symbol_change": false,
  "container_id": "tradingview_sp500"
});
</script>
    </div>
    """

    components.html(tradingview_html, height=550)
