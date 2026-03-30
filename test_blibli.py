import requests

url = "https://www.lazada.co.id/tag/sgm/?_keyori=ss&ajax=true&catalog_redirect_tag=true&from=search_history&isFirstRequest=true&page=5&q=sgm&spm=a2o4j.pdp_revamp.search.2.44d3367clhKmSA&sugg=sgm_0_1"

payload = {}
headers = {
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
# 
'Cookie': '__wpkreporterwid_=d0f62c5e-1eff-45c7-a4ab-99abc4067d72; miidlaz=miidgl3vcs1j90s7lepr44k; t_fv=1762039933572; t_uid=zZK4vjlaQojkbsmlB4FiUOdoVtyHCIJW; lwrid=AgGaQcOrAVp%2ByGA3cSsLX39uI5Qx; lzd_cid=f6e5d77d-06a4-4e85-b04d-87f843e91374; lzd_click_id=clkgg5vbk1j9qnl02145te; userLanguageML=id; hng=ID|id-ID|IDR|360; hng.sig=to18pG508Hzz7EPB_okhuQu8kDUP3TDmLlnu4IbIOY8; __itrace_wid=77f6df93-7f39-4af5-a9e3-cbb122738a57; _bl_uid=89mb9m9db2zfdFf3sc7I2qp0pI4b; isg=BJ2dpYoCqJucoUwWV2-hflw4rHmXutEMxOh8519ih_Q0FrxIJgol3FRFRBIQ1unE; EGG_SESS=S_Gs1wHo9OvRHCMp98md7FWq2FVz6tfLS6v06vH8sU3TszpGTwbRo6nHqPpFkgsQCStxu4jWAS-7kzknCdEr1G6hGL4UM99uZqMKuY7JPknB5vGsqtko5yOOsyWWlOYkEzsiGuenBVQqcEorlFbfL40JoN_Yt8t2OI5OKgSoyVY=; lwrtk=AAIEabF19dqIzmdElvkeaBwjWHkeLmzLBETS7iMLF/N2Xqzy/DHRjFQ=; tfstk=gkWqpWOeS-eqno4hYMvaL8nbH2vvKdzI0OT6jGjMcEYmhxgGaaQZfoUTM_8NrUsfCKXNwASdXtZvCopADdpgRywN7iIvBCE8VfXqZYxFqhcMi79uZ5uM8ywQdijcSBq3RsOoHNxMjdxDohmu4H-6jdAMoYqyjhgmsxbGqu8JxnDMSdAorHxemdvGSgqycHpMSNA04gYJjdYisW1f1b-Hio4Os7L0lLd2-iYrLwBym9hA0UuSyT5P2eXwzADGznjgb10nL5Th9EOBla2S3dSkbw-Fu44yIgWALQX0yARR7UdNUQyz8gWwuBXDaDHOVgKGSC588vt2h_RF3sEtribBu6vAfDzf4B5y93AobjvfOM69tt2qJUOpbw-FuqSPPVKuEJB9a_cwi3KyRurrjq5wmYzeAyGt6QYe4eZvkfh9inxyRurr6fdja38QDlC..; t_sid=qHhRHSf1dNRuFJGmEqYCfUXeI7Xwjt3K; utm_channel=NA; lzd_sid=1a155993d3bc8c1325584cea19cdf084; _tb_token_=e53a4eeb3bb00; _m_h5_tk=bfbcbf01793f2988f92e4804b624482e_1773228014832; _m_h5_tk_enc=562c65c92d4495c41b983545a02e9d66; clkgg5vbk1j9qnl02145te_click_time=1773220090414; epssw=11*mmLhKmqm2XZ3gRAzEN0dWhn0WnCLtJjGuiSfY5WWXLxtyzI0S_1fgC6ktyncmuZ-REQJ1rT1po8kc5fvEOMBUmA4Y43vQRAx3fjWQiAxpEAQe5kF7LOUhX_YW-Aur6a3mDRkz1BMammmmCHKxt_U1DRsVGymNtV3M8H4KtnDijDcQJXP4h0u5paWzyFCzucniWvMnepqPaNBP8JE1_7C1zWmuuMCtnkbiammmmXmSRmmqeam7D7tStF3fDv0NRemfDZJuw8aEmNEBBBmBjaYNtym2PmemvgEuu7nEHLxaYIJhXMJf-N8mvfa'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
