import streamlit as st, pandas as pd, numpy as np, plotly.graph_objects as go
from pathlib import Path
from datetime import date
import io
st.set_page_config(page_title='NEÀPOLIS IMPACT',page_icon='◉',layout='wide',initial_sidebar_state='collapsed')
BASE=Path(__file__).parent/'dades'
TABLES=['Projectes','Inputs','Activitats','Objectius','Outputs','Outcomes','Impactes','Hipòtesis','Retorn territorial','WorkPackages','Deliverables','Milestones','Tasks','Economics','Startups','Riscos']
EMBEDDED_DATA = {
    'Activitats': 'eNqtls1y0zAQx+/M8A56gM00tpW0PYYk7XSmdDrTFI6dray0AlvySHJoOfEa3LjRO0cOHPImvACvwMp2EkOZUAcunrU+Vj9r/7vrH1+/naRXhTVvpPASzky+eaEJFF4tlEcPo7U1U0XpWjNHSmNWWRP0eKW0Eqo254qcyYVyHuEVZsZemevgWpVwqasd9Sg6Z8gDTGmhf/7svB/BGHM6haXfP3yc5uREy9RYhWyinC2L4GFEqy5kJoVQyy9MsVThjTaOjl4Zx7TLomVEkC4ftKDtiuEC9fJzGNUsQzZLxxD340GvP+yRw5WZ9GEIRGN9WTgym298jyk+nS+GI2NzbPg8Zpm0jnYWNOSr4Y6I+2vEKOpFAzLBSeeU0Q6iA5hqJkrrng6YwEupPQ1LxwpiM6uPlG41g/+CSLcYEeOtseQwiuLuhBzGRmt5F66wCUdPhsUO95ReBGa7WdKR9XDDGvfoKMIVtatwofGwO+4AJjI3bIL3pMJ56QL2HsulFaT1TnA1UcscQqG8uJV/UGMMZ9K/M/Ytf02PKjFGevkpU46yQmbMUQLKHFlmBGbVBxhRFrUAd0mWkCm1/IJZJUsE6/SL/ooXh4g5r3y5Tl2NedhQvV+eHsOxodjq6vCOZEkT1INgJhEJcJMjvB3RR1gJzKy5DuJn3qJ2mnBCRjgYVeHWVJxuZHcc3sYZgm8OgXgrDYdRikVdJqoonlbRI+ll5j4nGEbFpcyJmVDn0tYoHel4c1n7QWRENwAq/ouQrFvZBnBOblJZ39P68FpgYU6ruRKdK1yoHZvo8VpXRYbQb9MkMOaz0en0bFYp/QU6mSktWx2gkrgUptH9ThpPNg2BLinuxYfEct2c9Vjjv0DF/11ISaim62LVD8nXEtJwK00ClFDkWRhhZROT3bIraZdMMkN8eKsD8a0cHC5yaoHsgjQiWfidCJumd9R4VNBzZ7nwxz2br/S7HaXRL6lkVP89nGgvbyzV6J21y0NYWu2EIlRr9zep/AThbDxR',
    'Deliverables': 'eNqtl0+K2zAUxveF3sEHkAf9858syziUwhBCCWQ5qI5mUOvYxnams+w1eoJ230UXXRQ6N+kFeoVKTsbKoBhLwpvwhTj5feg9fe/l36/f73a3dVN95HnHwara6zfyg+1avRaFODTsQ3H8XL/LWMfk4/xBtB07vms4K8Cat7c1b3JeduA9b+uqbPvnl/Kx7vWrNUTgmu3rQxvs/n75utzLnyj5rmoECzLRNoe6EwewXSOQoSsEbp55AQr+/Aze8rYTTz8CEdxXD7wpWfn0jQEMcRTCOESLQWIICLki5NxCoH71utrXBXe3gs+s4CkrSQiplvHMVsiZFTJtBSWDnPNUMMiwWaBMsPuyaoX0UhesFHciZ7n0drKQ6oNJxw4Ge7sxajTpZuiYNMR4ZjdGmSbcLEKItZzxbAjIiFmp5SPPD/mxbfijvLFiL6/sS0OyXwZJLhoi3oaMYk0aQjCEkZaLmQ0Z9bIxhNJBznlCFGTULNmmYWV7x5un72UuvyCCjpU5U6ZOJpA+IDR2QNTbj1ExCz/PHaRkNLMfo2CTfvAQP0piGz8YrHj3uWo+0a18cR9McQhRSOBJSiqyieDLVPsZJFE0RETL2J9qP27ifgjHg7QbNwbVfbLEKqFQpGVqk56XwU5DJO4bOwEjuDUvd7L7xmFOMyI5tZIHzGsESF6k+nUk1iZ5rgmf9NsK8ea5Bnhy6hoPnk8+Jyp0xnB0GucYv6lKGxx74xzTVW12o835AicHIt28uVmuNu5pSvrdiGhplWsm0T5JibrhxxW6lxj5Ee1TlKprjomWqTPRPUGpKh+OB0mgTYKaUKf0pP2Fh1pGflCnFKV6VhwlcYZ6pSntr386SLt10eS6782QnK7MUSI/rvt6rKbHQsvUmeu3Bau/dUj/ybTagk2s+7IL1YY7SOqH9dlpCTqXk9j/P+jW/g==',
    'Economics': 'eNrFmE2O2zYUx/cFegcfgDb4/bEMJg4QoB0YbdpZGqrMDJjakiHJbpe9Rm+Qdbvsoou5SS/QK/SJlCtrJNmjyEpgwKSlGfEnvj/f+5P//vX32816n6UfbFxYdJ/u6h9w42FVfu/So9vZpEB3UWEf08xF643N9zaP0CqzeX7Yp3mx3m+jxL13cVSgt7t9mhXrON3Bw3ZPH/PTlX30CLe/TRO7idDrqIjWLnGxW9utfXQ/ua0r4La//v7ZxTdRXByyaJ2uPxzywo8DQMuj2zx9TGIggvvu6P90efZ/8Db26PIiglcroq+/WmECb7HbH/LZ5p/ffl8CoAWY8p1mr12eHfaFO6CHFUFLsiBoZbM8TaItIlhjvMDQUlm2hjOzoGj5w3eIYirmWM7hyaGr5kQhAp9Xs6PNPGo2y2HiknwWp8kxhSl6+gNGRG8cQMduIBZF39vsaF0+s78WNktyJLGHEyo0lHNovggbQz+6qHi0+czNMntIHDwYMem5GKe+IVwu+EU8PBUeR3fpDqjiKHZPfwJjtC1AwUMJ8SQTCHKiDc0xETRHNRVlS5QxjcB6mNA1c0wnCqznaotOBTpFPJwUQnwptk7R8YDHqSq5mGHsCh6eCq9PdAMJpxEdQ0vWEJ2kQXSCGd9yIvRCn3F5GN8leE70RIH1XG3RmZDptBBee1rKxpx9RrZO0QkeMjBhPrKKmIW8iIenwusT3UDCaUQHuZU3RKdNEJ0yPosQKYg+5wowoUvnmE8UWM/VFh3BYaUa41eqIUqdq+5zwnWqTrIQU6NLPFga8tyadODhqfD6VDeQcKjqKLq3xS9p9jN/gK8O+0aJrLIa8RW+LKWsITBSlXhZVnsiB8ewG6FDS7TKYGEdQtmkDS1Nw9EpGxUyvcAch/pDGkFpk+AbkPQpZCDMaIU8N1uUsyoFYeJbRqWq695pXOgqQJkzPD4yPb7qZPsMDzWOKVIrZDKOToVoEoIilS8WnNJ6zXSS4BuQ9ClkIMxohTx3RlSFlft/seKKn63d07iha+ZEjI9MjwkioiKp6pIm3qpNDdIpkcqQVQmeG8KvkOAbkPRJZCDMaIk89zHUhB04xSqYZwmFp85jp3Ghq6HM3WTx9lkWWe0dSXDKMDOmMRfTgHRLJKwXabzlBAMq6s11Jwm+AUmvRIbBDJUIQ3f83atvlvfvug6RLttcVh808FKslA2OSnv4gW52EobBprWTAo+k+BRv2gEyShEt11H5UopF8KVaK10L8jRm6H5SKm8P3+9JCeFVXeFa15qYhOKSI5Xam0BJDa0dWCcFHklxxY2+FGSUJlo+o3KilGGvSEoo07UkeZ2kYL9ebtnHRaPPY1w+fJyE4pIHVdKUGAoqa2N9tCnwSIor/vOlIKM00TIWlfekQoqgDUhXjZMvP+ZpC83IuGj0mYqT7+RUhD0SIXhiikums+8UsE2BR1JcMZwvBRmmif8AMDdcyQ==',
    'Hipòtesis': 'eNqNUs1uEzEQviPxDvMARm3ShHsUIjVSGlVqgGM0sSdlWq9tebyhR16DG0d6pUcOHPZNeIG+AuONQpCqomqtlX/n+5vHn7/mbp1yvCFbyCxjc1zowSdO3Y9Cwub872yaubDlgsVc5rjBDfu6WA/WYzNvEurTfn5BFgNLQ+sdZd6yRcvdg5mJXn796vJ0YKbYpFbA/f7yddakTIFczIzwjiW3qXBrzvXWAqGhUPqTTJJiAIRAlkQqrugmejETX9CM9LvCwrJFW9GAgXbRt/18dfpmdWY+oGeHDiFhtoy+1n45naFZkICNIdAdxyCwX6nCQnxHAXTEFHNpQ0/OXHC5wVCZjc0VXbdc8eDtyWCoqiSKmQWQw37lMTRLKp9jvh191F/vwMwLqK0xCzQYihILlX1NIfWmghYqHK5bh3sfxoo3UX+kdN+DqlQfbFRNseEXYQ6r65sY1KXcfbOKhNDdC5SMQbYa58aTpkAqXUvqVY87PEQwrn2xU2MYtkRug/b2CeKZmY5Wk8VsueoVvg+1VuVLDYJ2iBqYYKs+arqluz9BRW6hoNf3R5x5cMrMVWMcHU7/C7XPrzZHDc9Gq83jdEe6B20rkbap0gR8tPvW+CdALXT0UMUlr2Y8009/ADzyOHU=',
    'Impactes': 'eNqVkr+O00AQxnsk3mEbuonOdgxJG/mCFIkLVwQoo8nuEA3Yu2Z2DVfyGrwBDRUlBUXehBfgFZi1A1ecdEBj75/Z3zfft/vz2/eN2/cS3pBNBNvQ3U50g7sex+H5/xLbIPtwyAU8nKe6M2ALLzwnTHCJCfcdxUEQdtwPcU/v2Z0+e8v48MF1UUKDnS4b9+Pjp3XXC3lyQRjNJUcZ+szdXOW653ZQVT59NegcWw4eW3PUckGHUM2hXMDT3RqqonoyK6tZUUMTfBI+DPnU/4hV0AjxDXXkk8Gj0BGTcWReZ28yNgHzAqoSHt0nV8GW0ocgb+tX+jnbuOJWU0LTk1g6DA4z2IYgjv1krw1W81sWUC8n/lLhM9X7B36VizzdaDrRhN+JzRK22YpqRo5Jh1G5sABsGb2leJ/KHJp6t3q23u7ODhrMVL3cqdMxTEyCg9CFkNJZzCSYTSzqycTjHNK8/Bu+gpW1Y/eb1bVhb4P0GpejaDSz0J6+JH43ULzQd3kU1JcF5ehkOvXnOu4o/QIg9/9c',
    'Inputs': 'eNq9Vb1yEzEQ7pnhHTSp14l9/k1pHCfjmWBCYgOdR9bJjuBOe9GPSVLxGnRQQcNQ0EFB4TfhBXgF9n5ixyQwASe5QhqtVtrvdr9v9fPb9144Sgy+lMJJ6GO8XNCG0ol30MvGgUq8LSwHBmdy/jlEM8IRGjWVGp56rp1y3MFQZ1PXpuMOd3wUKpugVmMVZTt9JJszfP6BF6aHDw7KFejwmGKw8Mebt904MVJLiqA421HW+MQpDz3y2lWaazoaS+1YMv86jpRYMcLRkw7bYkYKbyxaFqHgkYXtMn3QHR7CTgEnkhCUg3qp3Chl9wqnhGIn9CNMIwulUTNOE5vgMhK/OdQAuideJczNPwqtBOvL+bsEI2WZYgOuQ6k1HF6APPYx1xaWPlsLnwYkkny0tPeFvAovuDnNbkgTisbC42xWHLoCrbJOxpzJxXmoBHDheU8Ya5BtWZmmU+lZmiKKvoR3BanldEcElRagmXIi6TkXCvW9Ia6TJBKucrwTw6V1xgvnDSeJra4XNIAKyOUfrQ00oJvdazSvas9puCqn4eGjdmfAes9WBTXsEh3zPahXW41WY7O5nUqJ0c5pSpXfoKW41oUWwBEKypb0BhPpbcHJfMmhgNMEm3rdQfxqEYLtp/2D7Rn0CexR4zN5ZvK+Au0wVprqY4hM8y+lgmklGXqRW1J8Mm17RDxOndLdBdga5CiJfBGeZbXcReNj6FDfUKcysxBGbSd0axq4fzb/ZOT07Hj+/pwTzWLpMMQIp+ouillfUaNAjTGpYxzx2WWdwgEat0jhBE2cpzCRVvASNXRpBIegfmt5rEKnNmjvd/uD/9NCs1kLWpu1+t+0UP13ma7AupkOKuVrhbBu8BuK4FJxHY8oTRdFhCC4vljrAqvBRgdThik9Beqnwo8zrlBzFcqT3JijfjqW4cafmysVMveFKjiVZOSXtw20Du3sPdAUZypzDers4aG8XVJnUdbFyQY4g2Merg/oFyuegFg=',
    'Milestones': 'eNqlljFu2zAUhvcCuQMPQBYkRUnOGMROECA2jMKAx4KV6ICNTQminGbsNXqCdu/QoUOB+ia9QK9Q0nGRJyiRRHsRfoGyvt9P7+fj35+/bvL3ZVV8VFmt8KzYPN+4heXcX1e6lvulvRjLWrqH1IO2/+8qJdf4nbJlYaz8sFZ44pbqszdzyvCl3JRbi/I/n79MNu5nRuVFpSUaa1tty1pv8XLO8JS9ZfjKvR4x9PsHula21rvvSKO74kFVRprdV4k55TGhCeECSsBF/lUX1hZrnctAPH/C8z58SlgK5el4jqe88e/HWt6ZwmrHL9fS6JXOZOb8HLAjQs+hbDrgxzqABehxcE4oh/J0BxGeRo0aTB5Vts2ePoJ6LFWlN8rUTRM8hrJpIjrWBCxDrwlGCRtBeboJgaeiUYlFJY1dqWr3zWTuWY1qaTLpjRzAzLGhbHoQx3qAhej1wAkVUHZ54Him6k9FdS+W7hIU/8R1G+Ecyq78vUwalPTE7y4sgTKIFBTqxHcPHeFWkObK5K7IrxOGhjYllJGIhhFCQ+kgsd+RWynohQSELvVxZ3EYJDBUI18tmuJWG/cyhofGMcQLX6TBiPClWFzcTmaLoJRE+x0xhbKrd9uUQQkRvkg8gnIwJSgdYt9WFMqugdMGDQ2JOLQWkINBRwwwt1kzKLtmR5sVNKdo/HxmiNtnhg5W8DjyJwIBZdcoaKMCp07EoHwd9Q9VvpNn',
    'Objectius': 'eNqNU7tuE0EU7ZH4h6tIdDfC3k3iUFohQZZCsFAEJbqeHUcT5rGamTWBit/gCxAFFSUFhf+EH+AXOLN24jxcpLHmtedxz/G/338mzYc2hkutsuaz4DYbXIRZWZqO31wvzk3bpc35NJoQTZbM78SGuLlYbUXlTixPfGOUNDhQVrqnT6aDIR+JAxI1f79+O3Zt1F7j3gi9NCl2bc855Ld6HuLyu0RS0ooqRIl0eZ4Ej20i0yMY78MC98tffJxarZY/50bxkIeDAY8O+RmlLDF3bSJxM3LGQpw8WkfFOycAt6CPtBBrmhUVOR0VrJPxCx0TjiBHBe/1lQk+7dzWUvFowAfVfSmhDdj4YmyN3DxeV82vcBwhKuocoqesI8Iozyy0pS7KzCJHh9Ehz5pH+3wwui9h/S0cGAiVXOgrPtP5U4gf997j524SVugi4LUXjz3ZoMDWaLJQGlTXbonhcMD7++CVC+0RYCkBSalJ2kZW8biRtsxaWzrt4TEBGz47fE0nIXaOcIZBZ32VVwLujrrEXhdCFxpgSA+31VjNr1dliNfBIcQsFky7N2Z2Ne6Cw/BnVhZya6D1gIcVbyInPS/1X+jeWM1He+fj0+Oz8zLBo6jB0nkCWjIpayfklj8SzWUR+qRI1t3WpdfXIT1s9ItSI1GqZ5yMp5j+3HjTPGTFKHOULmrgIWftTVy7o0tkeOOk4gpODhgoykhv4PnG1X3UmlHCNuAv2NcTlqYoRVmOVZkXTZDMRZQt2dTFAhfNUIy+5y8ll/8b7qT7',
    'Outcomes': 'eNqVk8+O0zAQxu9IvIMv3CYidpp2e1x1e1gJtQh24VhNHYMMdmz8pyBOvAY33mGPHDj0TfYFeAXGSdDSRQhtpMR2PPnNN58nP7//uOx2Prh3SiYFG2fvFrThcpLOKthO4ys0LuzcvgToPC1RpowGrnudMMEFJtxZFXPAgTDFPn70vOawQutzZN3tl69r64PqVeeCRnahY8i+ILcrCnuZMKTsI0O7Z9Z1yrADGt0R/qyGhYAnIGrRVlxU9Qy2/AFwcQrvHX0hjVZ9iswxr41LEeYttGf3kogHJGngsj+oEPXxhvmgD9ghlbHXRqfPNAfe1uUCzsdxff2i5JpX9bxq6imXgI1KH114P3tNj9GY87eDUOMkmsg+ZMWkc16RDBaUzIEmydJdbGrbsQKiLiu+nGz6mypgbZQduJ1iBtne9Uiyj9/o3CQyEuzpYCOQWGjuQ/8htYGtd2Tz0BPkrMwepSawiU/fuGAx6YMi513fU3tgpyJQ4VzA8OYTRcaTNE1J08BqdnX+bL25mtyQBRlJq/IYCoSRF0xbPxZEGY83g+zlny3D28mLU5747e7QdNpQaxd3Q6f7EbRoYcH/zymHr6WeKiRLExriMvpNSieoUhjwOei7qBMkOfoL6fspfA==',
    'Outputs': 'eNqVkktuFDEQhveRcgcfoFq03Q8pyyiJIFI0E4kZWI4q7hIYuu3GD2DJNThHlixY5CZcgCtQ7pgJE5FF5Fa33PXX57+q/PvHz8thN3v3gXQkWLnpYcMBl+KcIqzvP29wdH7nbnLYpLJFHROOsLUmYoRzjLibKCSPS37RHh9d1xLOcJpTEMOvb98vptmTpcF5g+LcBJ/mjFxvN6x7HdHHNAfxKZHQbppHimTFyHkmGksevYGeVyhCULXqKqmquoW1fM5hCl45TywjMZGNWQFS1SClgvc5UtCyaupnohs4c9bSV+NsEMVpRVkf8IWxn8kH54Gxqge9Vx6UovJ5ClYUvzj/sX3Lr78tohAW8PbqJRuGFkL5kwF9VZ9U8qQY/g9Awca7Gxy48ujRBouac3EM3FQFscQKqq9U97SXBk61XqyMTjNBROJic3YHEvA+dmBqIXF32s3p1cVqUyp62lB/YIibU1eyK7U9wqiHxhQ3Q75B2hPz7m5Btvn5t1VddrWf7SNcA9cjLnPONd7diksb6Z3ney55zSPup5UNNcdHfwBdHRaP',
    'Projectes': 'eNrFlL1uIzcQx/sAeYeBqgSgvj8vqhx5HRxw8RkX+VIuKO5InmSX3JBcybrKyCukSndXXZOr0l2KFPsmfoG8Qoa70lo28tEESCNwR0POf/6/If/47ffnSZxb8x0qj+LSZA8fS8oL9/AZaU9e+jilBO3Dl1EyFeVdtiIfe7SWvLHEoXPpZUyaFNXLNYnIhR3Ngc2mrHzrSYkrazZWZiFVS12+lxlqz1F0rsiN8/GttLcyNvHacJylrizGzihyHFuhxjUXk5acuOAD0iBPXHBqnBerlJTkLazDW8lHr6j6/9NPrnp9sZAZdwrJ/d3PUZZbPikJPcA5OVvknopGGuSUGl9l4mkmaW22ktdcBMu3uUnJQReWUieo9UmMmthrSmXYxKFUwleYelt+FIPeYNzuTdqsqlr2B+3e6NjPG24o+puy37xcwP3dT3BQitwOQvDNepApfzjUW5MWeeUq1NguDUhlMQlWgDIZcIMHOnAdiQkwMOuL3MFnnKSo/BWCqs9F68LYTIaAgHBeUCNgyyKTJmoVy2WJW7Qu7CQ4x8zAudy3xI33ufui293tdh2NsvKmw/ldVaFon5rbTg4YtrJdeZLwMe1E7rvia/Qykdwb5OVHZvxDgW4OdYTb36DzoXKCaejLG0858JD48oMidJ1Af8Bw/M7Y70ff8o+4fvXl2WIJSyu1W6OFw5/icl9+sLjZ35Tv3khYkN/DjvwNLEyhef2KNjfe/TVTnoOGv4gKa3LJoX/A3+8f8M+YfXvY47sGeIuqqJxtvVQMsTbZyzTAJEBltMl4IiqurWMbz1+L1uRZrzOeTsW4D/c//gLVHZrDeDjrTGYTMX1WRa+jlphCdZcAg0QsnDiaQJYrsM85DwOwlS9CDeBBTM2+GiYehiKbw8Yw6vrmQlaknqTiwZiDOQrmY2rFDf/Crjipg0VX10a742JU2f4AmHFW0oFrEDMMwSPqqulHxJ9AHorFaHn2IrpcHp05U56MhiuGoElv/gfOwyfXfNg/veZn/Eypg2cWPWpVD/LBwDk8fn74XeIrf4p9Npp2hrOZGE0fYZ9OO6MBR8cN9n7vKfdIGUeOn2W2di23/LqsUl7KuqbD8Io1D0POl0Sy2MLiUSrPy79jVqNDzn+C+E+vTYF6',
    'Retorn territorial': 'eNqdU8Fu00AQvSPxD/sBE8V20qo9Rk2QIqFQVSkcq8lmigbWO9bu2vTIb/AH3Dhw5MAhf8IP8AuddZK2pK0Q+GBrPLPvvXkz+/vHz/n6qgnygWwiWEh9H2giUJLgYco1+cib7zD3a7a4lrBPvUWngazyEW53IdrUooNLzwkTTDHhVU2xDfjyxXlRwhnWTRvN+tfnL7O6CeRJARnNlGNomwxzsdSyN7Zt0CqrYZPQkU+qT885J1ZPk0mBVuic6djb1mGKBp1JFAKrNIbyCMoSXi1nUBXV8aCsBsX4HwRUMLPipWaEKcWGIg41TkGb26rCemXUrI423/S46hKLLiptoY9Sn+TP7PLi/+hH6rWXrqeCc3aScs+RfCdOfXnUbAEn0PRlB3wVLCh9kvBx/E5fW2u1s8gxUY0wcYze0l6+0fa4IwVR98aAu+wWszgdlKdPY1ZPjetMvKcbFh93fwbSSEhtvxd3ho3UrArsXe1fuUYZmPiG6kwyea/vaK4l1Ao6ZK+mWPQdRxgXUJWAfcEBqmKMl5PXs8Xy2WWbe7aMvRv9rDDPPpcMdffJ94OpVPsx8H1lpjnK5o/KxzTVQ+MXkoH3BhsxVnQZdN+i9O5n5Q/cfxb0wA1VmP3urwf6eE1h81W1Yn8dRoDb/B+It6nYYPE=',
    'Riscos': 'eNq9lk+O2jAUh/eVegdr1o4a/wHa5YiwGKmiCCGxRMbxjDxN4sgxdNtr9Abdd9lFF3OTXqBX6PPAlGmUoGFsECiKFcf5vS/yl/fn56+bfFVbc6+kU3hqysMALixn/mh1I/HcH2bWrMVaF9oJtyKrAb4pawFzH8/Hwqk7Y7XAmXBiZdbKuo3dj5yopChV5fBcNbWpGrEuFL6WUj/8WEljLTzSwORJA0u/fTNLCaxX1psG5b+/fpuUtVWVyv3qKNON3dROb/ByRvCckMdsKFfwb7Za+CX9SIpCVbmwGhkY1nD+8L2SEI/Db/x0EdOUDpJ0mMATn2dDfvGruaoLUelbLYXFSDSNvquERfbZPI22yu5moFsAc4UXvtbTisj+VWHkxmMSBXqH1FbvMyNdSVPWhXICU4ifPU3zxR4tYby/zR5WUw0Sa1FBKlWgw4s5NTYF9vRU9oMO9qOEjNrB6YXYU8+eBrPvLuF87BmwZ6eyZx3sPyQpbQdnF2LPPHsWzL67hPOx58CeR3AOSRPyvh2cX4g99+x5KPueEl7DnuKpcl+M/cyXcNhZkcZQOyER1f7Jf9T64mY0WOI9YV8OtD8gSI6G63rovzNkGEvXR+NmNFDMvWFj8ARx0XAFj+B9JyyNpeCjcTMaKNvesFE2PNiIhnt15D8IZBDLq/1AvUEpDwbaHfY1QOE18MX1x8l0sdMRC7cnO1dj3M6asUB1spj973/pwEEs3Jvcbx3Yf9Hb3HbWjAVKszdpMEmwDws3Ju/eMywuSa9LxoJJdicNJgnaYTFa0NS3z/Fb0HbWjAV3mj1JTyf5F0DN7po=',
    'Startups': 'eNrlmL1y00AQgHtmeIebFFQ7gyVLljxUIfFAZkwC2ITSsz4fcHC6E/djTMcL8AA8AVDQQAcFhd6EF+AVWFmO7YQJGCadXNj3t7e7n9a7a//89v1oNimteS64F3Bsis2ENpxH60O5XD8bj2jTWBgLayUNJOzr1xNuBXJZfYETHsrlaDLuwMm0vkmGteyRLoOfcIUBToLfHnNTiGZyVNAFfjW5K8vqsxdONtOHgjTqiT/TjapZr97qmVhMONa6PXpXa/99ke4NqMib4EhOCu0dmTQX1tUG00GPM5wMHj3ccmMt43HiLVbvcSpVfd31a/c7ERxgUQbHZj/evBsUpRVazGq72KF0NpTkO4zolODm0JAaGBnnhZarK+BUKtRmjkwyheyOUN5WXyHuxDF0YeA4KrSsMDOh6EQhLCeZfc6rj44hs4IH64yjrQXaBcJ9giy5bAy/OUclZ81D2as9Zmces1Iq4x0zjE6g5sLtwd6B0c6sBZg5858up2crF6Ig2T0YIuNGa7Got7CYMvLMSfKpQPaUnLfITGnoWesl8Q1HdpNJXbu6mmzkIOlDL4MIok79gqSONnIOFSMQ6S1WVB+8lS+DcOyJ5L76xKVwu9OP4VQs6njl2ijzVCJJeVRBv8aadJcUtoV02oUsghiidEk6vWLSXbitcKqw3IZ9aYgnpL814DPIUvpKx02I964YfALjYKUrTtipnAvNKS+uVsT5YE9JdVuY9yLI+vTljptgz66YeQoPppKKFowIryfVt6Xxgj+7PODJnvbATyHvAqWYJfv8itn34JTsWVya02PKca0h3Yd8q3r2d0Ydw7Hwr4x9kTymN6KaUfoOYvRCKuXYEKcwIGNNQewpp8//kMm7bWpWcuj1NiW0C6Omta1d3pl0DvfQHlLEsoPaPu63IpkVaKtPXhYXYjppU58SQ9bZlMvkvyD3SZVAPUZFdkLzQWrWflwez2mbOpMeZMmmSqa7oO7CQTLeHw6OxzCKOiu0Q2PK1fB84EZt6jmoz8jXZa/3zzAjGBoiRdngGbsbpjv10XGb2ooE8nhT7LJ/BhzXfyEEq2/csebVJimIrU7j4s/DFrUSOeRbtS3/O91fZvXNqg==',
    'Tasks': 'eNqdmE9u3DYUxvcFcgcdgFOIf/RvWcSDJEBgGIUBLw1WQwdqPJIgadIse42eoN130UUXBeqb9AK5QkmKIiVLIz1qM/hmxp73E/VR7+P79vc/H06PdVP9LPJOoNvq7N7ILx7u1GvH25zr73p1wzv+WJRFXsg/Fl+KtjOfPS180Aj+jN5XjWgf62deFk9Fzk+iRXeiaatSfiq/qauy5T89y09/dG/kTxVlXtTy329ELcrTyx/yLUdH+evdm+/uQoze8nN9aYPTf7/+djzLyqU4VU3Bg5uibS51V1zQwx1G9/h7+aLIAxz8+1fwTrRd8fJnUASfqi+iKXn58jtHJCTRIYwPIbUSh2MZRYiM+QL12+htda6fRcdP3BOJGCSyjYSZlQQ7SVASLiDpy92NRQ0W3cYisZGJWzQpCUqjZSyyH4sZLLaFJQESK+3CaYnDK8tFd3HJG0imxrop+KeyagsJZq2eS1AHkVk5WjwppbfoKzKC9lNNvLVJRQdPpW7tpEyVveZU+qJ3k03stUGWHrAjw6mTiXLYIhnZTzZx2CYZoVbScCyVyRbR9plMrhedmuz4VeSXvLe/+FqLpjiLshvTZYeQWWmXUEvpM/wKjqL9YBOfQcBwZKV8fFlJldXmYPrSd8NNrAaBI8b8OLQLqCRVbluEI/vhJm7bhFMYqZXDIvZSGW6Rbp/hJBibGu6+4WX7JJq+/UrEjpc5V4QWg4ROJmO50DMZ2s818dsmFz6E2MnUyWypcZoL3802sRuADRMnMyfTpe5pLn4328RtADYy2J+4JdRyqYWaq5/CEXQrul+q5jN7kC++MWy8POSA47GExLDl6rDEJRPg4BYpiXmA9hKeuJYJYOFKZdBDGBnJHAxT/RkarpYJYDlK1orMnY91JmZjCc5RMwS/yKTr9c+T2OWUQUIi0zIAOB3FrtPHukHEaCUTHcsgvzTt9brg7BPrR3tmJFatciXxbNYFJ5tYbzFtvETtAvkwWssza4W9c0uiN1hoJFU7/Upa2Szrk0oSt8ESZXq5xVeyyGZpn8yRuJ2V6HNLilaSxmZpn0SRuO2U6LxI0VqOWKvtmxcSs5G0lDaXkflKStis6pEGErONekmGnXwlA2xW9uj1qdlIvSTqAL/S4Tcre3TyVG+jyEhmd/OV/j0qLZ/j7P6Hj8fbe7/GTfWwghiZmMseJKRxzyvDmjbV58LQyOGc0csY3LTn1WENm7qATnV2oU7CpyHz6rBmTXU20zuKabPhsQQ360l5v0bNlLH7ERDTpgvHEtKo58XBTZrpJzgxMjL3oZcZeIQxBwB3a12KDoueuFuhGgp4UjEHALdtXYpkRmbuTmgJHkhMCLz7N3PPdeaOXoOEzB3m9X0aOXPnFqY2BA2dxODxwpzBc4qA3VyD2LNwqBsOdIowZ/AbFshdZxmYY9ASPCyYQPjPBOSOIG54TqKxhMwE5uW9jv6297ye1UmDQI/+cwSvE/5o2KVGIXg8K4Ge8OcIvgd5TN3RORtL4EH+f5OIFsk=',
    'WorkPackages': 'eNqNkj9uwjAUh/dKvUMO8CL5H4GOFaCqUoUyIDEiNxjkltiR7VDGXqMnaPeOHTpwk16gV6iTkACKSliSX+z4e36f3u/X9/1inhn9JBInYKLTw4ffmMXlkn+NuONzqWQiq7iU/kexkdZxiI2wNs+0dcWfsTBWK2HnfjXTyvLHtbDXVzHCMORplttg8fP6Nk79cSUW2kgejKQ1eeZkDrMYw52wTu4+Axms9EYYxdXunQNBpBeiKPSYKvZD3AfCEEJALscTGEm+UtpKz8/WXMmlTHji651gy3gTIgIUFRXo5RUojLciyZOqBbHNhJGpUO64SEkuI0YhHgCNiiL48iIMpoYruxRm96ESvykDx1XCi0LH4CqSEDFgpFFFYCLcizbPbOYfXdIx3kuPCv84Ajb4n3Teb03wse+hIUXQY43fFqxTZQ2p4k2IexChRmWL12WtZvg48MoKchQ1vVIYsuntw3gyPW+MHsaUFfcj9Nj9CeW8rfp0FcubVeppC9Rpih1a8/NXjODePG6xumerOl/PFsV76b6/P+kNVs4=',
}

@st.cache_data
def load_demo():
    # Prefer external CSV files when present; otherwise use the embedded demo data.
    # This makes the Streamlit deployment self-contained even if the /dades folder
    # is not uploaded to GitHub.
    out={}
    for n in TABLES:
        p=BASE/f'{n}.csv'
        if p.exists():
            out[n]=pd.read_csv(p)
        else:
            import base64, zlib
            raw=zlib.decompress(base64.b64decode(EMBEDDED_DATA[n]))
            out[n]=pd.read_csv(io.BytesIO(raw))
    return out
if 'dades' not in st.session_state: st.session_state.dades=load_demo(); st.session_state.mode='DEMO · DADES FICTÍCIES'
if 'nav' not in st.session_state: st.session_state.nav='HOME'
D=st.session_state.dades

def dt(df,*cols):
 d=df.copy()
 for c in cols:
  if c in d: d[c]=pd.to_datetime(d[c],errors='coerce')
 return d

def money(x):
 try:return f'{float(x):,.0f} €'.replace(',','.')
 except:return '—'
def pct(v): return f'{100*v:.0f}%'
def gohome(): st.session_state.nav='HOME'; st.rerun()
def goto(x): st.session_state.nav=x; st.rerun()
def card(title,value,desc,delta=''):
 st.markdown(f'''<div class="kpi"><div class="kt">{title}</div><div class="kv">{value}</div>{f'<div class="kd">{delta}</div>' if delta else ''}<div class="kx">{desc}</div></div>''',unsafe_allow_html=True)
def section(t,s=''): st.markdown(f'<div class="sect"><h2>{t}</h2><p>{s}</p></div>',unsafe_allow_html=True)
def filtered(name,pid,asof=None):
 d=D[name].copy(); d=d[d.Id_projecte==pid] if 'Id_projecte' in d else d
 if asof:
  for c in ['Data_mesura','Data_disponibilitat','Data_fi_prevista','Data_prevista','Data_obertura']:
   if c in d.columns:
    d[c]=pd.to_datetime(d[c],errors='coerce'); d=d[(d[c].isna())|(d[c]<=pd.Timestamp(asof))]; break
 return d

def derive(pid,asof):
 cut=pd.Timestamp(asof)
 dl=dt(filtered('Deliverables',pid),'Data_prevista','Data_real'); dl['Pes_percent']=pd.to_numeric(dl.Pes_percent,errors='coerce').fillna(0)
 dl['Planificat']=dl.Data_prevista<=cut; dl['Real']=dl.Data_real.notna()&(dl.Data_real<=cut); dl['Vençut']=dl.Planificat&~dl.Real
 agg=dl.groupby('Id_WP').apply(lambda g:pd.Series({'plan':(g.Pes_percent*g.Planificat).sum()/max(g.Pes_percent.sum(),1),'real':(g.Pes_percent*g.Real).sum()/max(g.Pes_percent.sum(),1),'vençuts':int(g.Vençut.sum())}),include_groups=False).reset_index()
 wp=filtered('WorkPackages',pid).merge(agg,on='Id_WP',how='left').fillna({'plan':0,'real':0,'vençuts':0}); wp['gap']=(wp.plan-wp.real).clip(lower=0)
 eco=dt(filtered('Economics',pid),'Data_inici_elegibilitat','Data_fi_elegibilitat'); eco=eco[eco.Data_inici_elegibilitat<=cut];
 for c in ['Pressupost_planificat','Import_compromès','Import_pagat','Factura_o_justificant','Evidència_activitat']: eco[c]=pd.to_numeric(eco[c],errors='coerce').fillna(0)
 r=dt(filtered('Riscos',pid),'Data_obertura','Data_tancament'); r['obert']=(r.Data_obertura<=cut)&(r.Data_tancament.isna()| (r.Data_tancament>cut))
 openr=int(r.obert.sum()); docs=int(((eco.Factura_o_justificant==0)|(eco.Evidència_activitat==0)).sum())
 schedule=float(wp.gap.mean()) if len(wp) else 0; overdue=int(wp.vençuts.sum())
 budget_plan=float(eco.Pressupost_planificat.sum()); paid=float(eco.Import_pagat.sum()); committed=float(eco.Import_compromès.sum())
 budget_pressure=max(0,(committed/max(budget_plan,1))-.85)
 risk=min(100,round(45*min(schedule/.25,1)+20*min(overdue/4,1)+15*min(openr/4,1)+12*min(docs/5,1)+8*min(budget_pressure/.15,1)))
 status='ALT' if risk>=70 else ('MODERAT' if risk>=40 else 'CONTROLAT')
 return wp,dl,eco,r,dict(risk=risk,status=status,plan=float(wp.plan.mean()) if len(wp) else 0,real=float(wp.real.mean()) if len(wp) else 0,overdue=overdue,openr=openr,docs=docs,budget=paid/max(budget_plan,1),paid=paid,committed=committed,budget_plan=budget_plan)

st.markdown('''<style>
.stApp{background:#f4f7fb;color:#10283d}.block-container{padding-top:1.1rem;max-width:1450px}.hero{background:linear-gradient(125deg,#071b2d,#103a53 65%,#0a6672);border-radius:24px;padding:28px 34px;color:white;margin:8px 0 18px;box-shadow:0 12px 35px #0b233326}.hero h1{font-size:42px;margin:3px 0}.hero p{font-size:17px;color:#d8e8ef;margin:0}.badge{font-size:11px;font-weight:800;letter-spacing:.13em;background:#ffffff17;border:1px solid #ffffff33;padding:6px 10px;border-radius:999px}.eyebrow{font-size:11px;letter-spacing:.16em;font-weight:800;color:#74d6de;margin-top:15px}.kpi{background:white;border:1px solid #dce7ef;border-radius:18px;padding:17px 18px;min-height:145px;box-shadow:0 4px 16px #16384d0c}.kt{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:#597286;font-weight:800}.kv{font-size:28px;font-weight:850;color:#0b2c43;margin:7px 0}.kd{font-size:12px;font-weight:800;color:#0d7b86}.kx{font-size:12px;color:#667d8d;line-height:1.35;margin-top:7px}.sect{margin:25px 0 10px}.sect h2{margin:0;color:#0b2c43;font-size:23px}.sect p{margin:4px 0;color:#6b7e8c}.risk{background:#081c2d;border-radius:20px;padding:22px;color:white;min-height:218px}.lights{display:flex;gap:11px;margin:18px 0}.light{width:32px;height:32px;border-radius:50%;opacity:.18}.on{opacity:1;box-shadow:0 0 20px currentColor}.rtitle{font-size:28px;font-weight:900}.rsub{font-size:12px;color:#bdd0dd;margin-top:8px;line-height:1.45}.projectname{font-size:18px;font-weight:850;color:#fff;margin-top:8px}.navbox{background:white;border:1px solid #dce7ef;border-radius:16px;padding:15px;margin-bottom:7px}.smallnote{font-size:12px;color:#6b7e8c}.stButton>button{border-radius:12px;font-weight:750;border:1px solid #cbdde8}.stButton>button:hover{border-color:#0a7f89;color:#0a6872}.dataframe{border-radius:14px}.call{background:#eaf7f7;border-left:4px solid #0a7f89;padding:14px 16px;border-radius:10px;color:#234a5a}
</style>''',unsafe_allow_html=True)
# permanent home navigation button
h1,h2=st.columns([1,8]);
with h1:
 if st.button('⌂  INICI',use_container_width=True): gohome()
st.markdown(f'''<div class="hero"><span class="badge">{st.session_state.mode}</span><div class="eyebrow">PROJECT & IMPACT INTELLIGENCE SYSTEM</div><h1>NEÀPOLIS IMPACT</h1><p>Control, anticipació i impacte en una sola vista: de l’execució calendaritzada a les decisions, els resultats i el retorn territorial.</p></div>''',unsafe_allow_html=True)
# compatible filters
proj=D['Projectes']; pmap=dict(zip(proj.Nom_projecte,proj.Id_projecte)); c1,c2,c3=st.columns([1.5,1,1.3])
with c1: pname=st.selectbox('Projecte',proj.Nom_projecte.tolist(),index=0); pid=pmap[pname]
with c2: asof=st.date_input('Data d’anàlisi',value=date.today(),min_value=date(2023,6,1),max_value=date(2028,4,30))
startup_options=['Totes']+D['Startups'].loc[D['Startups'].Id_projecte==pid,'Nom_startup'].tolist()
with c3: startup=st.selectbox('Startup',startup_options)
wp,dl,eco,risks,K=derive(pid,asof)
# navigation helpers
TDC=['Inputs','Activitats','Outputs','Outcomes','Impactes','Hipòtesis','Retorn territorial']

if st.session_state.nav=='HOME':
 section('Quadre de comandaments',f'Visualització de dades a {pd.Timestamp(asof).strftime("%d/%m/%Y")}.')
 left,right=st.columns([1.05,2.35])
 with left:
  color={'ALT':'#ef4444','MODERAT':'#f59e0b','CONTROLAT':'#22c55e'}[K['status']]
  st.markdown(f'''<div class="risk"><div class="smallnote" style="color:#9fc1d1">PROJECTE SELECCIONAT</div><div class="projectname">{pname}</div><div class="lights"><div class="light {'on' if K['status']=='CONTROLAT' else ''}" style="background:#22c55e;color:#22c55e"></div><div class="light {'on' if K['status']=='MODERAT' else ''}" style="background:#f59e0b;color:#f59e0b"></div><div class="light {'on' if K['status']=='ALT' else ''}" style="background:#ef4444;color:#ef4444"></div></div><div class="rtitle" style="color:{color}">RISC {K['status']} · {K['risk']}/100</div><div class="rsub">Índex explicable de priorització. Integra desviació temporal, lliurables vençuts, riscos oberts, evidències pendents i pressió pressupostària. No és una probabilitat.</div></div>''',unsafe_allow_html=True)
 with right:
  if startup=='Totes':
   o=filtered('Objectius',pid,asof); cols=st.columns(3)
   for i in range(3):
    if i<len(o):
     r=o.iloc[i]; val=f"{r.Valor_actual:g} / {r.Valor_objectiu:g}"; desc=f"{r.Indicador_clau}. Mesura l'avenç de l'objectiu {r.Id_objectiu}: {r.Objectiu}."
     with cols[i]: card(f'Objectiu {r.Id_objectiu}',val,desc)
   cols=st.columns(3)
   with cols[0]: card('Progrés real',pct(K['real']),"Proporció ponderada de lliurables completats fins a la data d’anàlisi.",f"Planificat {pct(K['plan'])}")
   with cols[1]: card('Execució pressupostària',pct(K['budget']),"Import pagat respecte del pressupost planificat registrat al sistema.",money(K['paid']))
   with cols[2]: card('Control documental',str(K['docs']),"Moviments econòmics amb factura/justificant o evidència d’activitat pendent.",'pendències')
  else:
   s=D['Startups'][(D['Startups'].Id_projecte==pid)&(D['Startups'].Nom_startup==startup)].iloc[0]; cols=st.columns(3)
   with cols[0]: card('Capacitats',f"{s['Índex_capacitats_actual']}/100",'Evolució de capacitats empresarials respecte de la línia de base.',f"T0 {s['Índex_capacitats_T0']}/100")
   with cols[1]: card('Nous clients',int(s.Nous_clients),'Nous clients o oportunitats comercials atribuïdes al període de seguiment.')
   with cols[2]: card('Inversió captada',money(s.Inversió_captada_EUR),'Capital privat mobilitzat per la startup durant el seguiment.')
   cols=st.columns(3)
   with cols[0]: card('Ocupació actual',int(s.Ocupació_actual),'Llocs de treball actuals declarats per la startup.',f"T0 {int(s.Ocupació_T0)}")
   with cols[1]: card('Outcome clau',s.Outcome_clau,'Canvi esperat de curt/mitjà termini vinculat a la participació de la startup.')
   with cols[2]: card('Retorn territorial',s.Retorn_territorial_clau,'Dimensió de valor local que es vol verificar i seguir.')
 section('Teoria del Canvi','Selecciona una dimensió per obrir els seus indicadors de seguiment i control.')
 cc=st.columns(4)
 for i,x in enumerate(TDC):
  with cc[i%4]:
   if st.button(x,use_container_width=True,key='tdc'+x): goto(x)
 if startup=='Totes':
  section('Trajectòria del projecte','Progrés planificat vs progrés real calculat a partir dels lliurables i les seves dates.')
  p=proj[proj.Id_projecte==pid].iloc[0]; start=pd.to_datetime(p.Data_inici); end=min(pd.Timestamp(asof),pd.to_datetime(p.Data_fi)); dates=list(pd.date_range(start,end,freq='MS'))+[pd.Timestamp(asof)]; hist=[]
  for dte in sorted(set(dates)):
   _,_,_,_,kk=derive(pid,dte.date()); hist.append([dte,100*kk['plan'],100*kk['real']])
  hh=pd.DataFrame(hist,columns=['Data','Planificat','Real']); fig=go.Figure(); fig.add_trace(go.Scatter(x=hh.Data,y=hh.Planificat,name='Planificat',mode='lines')); fig.add_trace(go.Scatter(x=hh.Data,y=hh.Real,name='Real',mode='lines+markers')); fig.update_layout(height=330,margin=dict(l=10,r=10,t=15,b=10),yaxis_title='Progrés %',legend_orientation='h'); st.plotly_chart(fig,use_container_width=True)
 else:
  section('Evolució de la startup','Comparació entre línia de base i situació actual dels indicadors de capacitat i ocupació.')
  s=D['Startups'][(D['Startups'].Id_projecte==pid)&(D['Startups'].Nom_startup==startup)].iloc[0]
  f=go.Figure(); f.add_trace(go.Bar(name='T0',x=['Capacitats','Ocupació'],y=[s['Índex_capacitats_T0'],s.Ocupació_T0])); f.add_trace(go.Bar(name='Actual',x=['Capacitats','Ocupació'],y=[s['Índex_capacitats_actual'],s.Ocupació_actual])); f.update_layout(barmode='group',height=330,margin=dict(l=10,r=10,t=15,b=10)); st.plotly_chart(f,use_container_width=True)
 section('Accés ràpid','Selecciona l’opció d’anàlisi que desitges visualitzar.')
 quick=[('Seguiment del projecte','Calendari, WP, lliurables, fites i tasques.'),('Resultats en startups','Última mesura disponible per startup.'),('Analítica predictiva','Semàfor, causes, escenaris i accions correctores.'),('Data Hub','Visualitza, filtra, carrega i descarrega les taules de dades.'),('Metodologia','Regles de càlcul, governança i traçabilitat.')]
 cols=st.columns(5)
 for i,(a,b) in enumerate(quick):
  with cols[i]:
   st.markdown(f'<div class="navbox"><b>{a}</b><div class="smallnote">{b}</div></div>',unsafe_allow_html=True)
   if st.button('Obrir →',key='q'+a,use_container_width=True): goto(a)

elif st.session_state.nav in TDC:
 name=st.session_state.nav; section(name,f'Lectura gerencial de {name.lower()} per al projecte seleccionat.')
 df=filtered(name,pid,asof)
 if startup!='Totes':
  s=D['Startups'][(D['Startups'].Id_projecte==pid)&(D['Startups'].Nom_startup==startup)].iloc[0]
  field={'Inputs':'Input_clau','Outputs':'Output_clau','Outcomes':'Outcome_clau','Impactes':'Impacte_clau','Hipòtesis':'Hipòtesi_clau','Retorn territorial':'Retorn_territorial_clau'}.get(name)
  if field: st.markdown(f'<div class="call"><b>{startup}</b><br>{s[field]}</div>',unsafe_allow_html=True)
 if name in ['Outputs','Outcomes','Impactes','Retorn territorial'] and len(df):
  val='Valor_actual'; tar='Valor_objectiu'; label=[c for c in df.columns if c in ['Output','Outcome','Impacte','Indicador_retorn']][0]
  plot=df[[label,val,tar]].copy(); fig=go.Figure(); fig.add_trace(go.Bar(name='Actual',x=plot[label],y=plot[val])); fig.add_trace(go.Bar(name='Objectiu',x=plot[label],y=plot[tar])); fig.update_layout(barmode='group',height=390,margin=dict(l=10,r=10,t=20,b=120)); st.plotly_chart(fig,use_container_width=True)
 elif name=='Inputs' and len(df):
  fig=go.Figure(go.Bar(x=df.Quantitat,y=df.Input,orientation='h')); fig.update_layout(height=380,margin=dict(l=10,r=10,t=20,b=10)); st.plotly_chart(fig,use_container_width=True)
 elif name=='Activitats' and len(df):
  fig=go.Figure(); fig.add_trace(go.Bar(name='Assolit',x=df.Activitat,y=df.Valor_assolit)); fig.add_trace(go.Bar(name='Objectiu',x=df.Activitat,y=df.Valor_objectiu)); fig.update_layout(barmode='group',height=380,margin=dict(l=10,r=10,t=20,b=100)); st.plotly_chart(fig,use_container_width=True)
 elif name=='Hipòtesis' and len(df):
  fig=go.Figure(go.Scatter(x=df.Probabilitat_1_5,y=df.Impacte_1_5,mode='markers+text',text=df.Id_hipòtesi,textposition='top center',marker_size=22)); fig.update_layout(xaxis_title='Probabilitat',yaxis_title='Impacte',xaxis_range=[0.5,5.5],yaxis_range=[0.5,5.5],height=360); st.plotly_chart(fig,use_container_width=True)
 st.dataframe(df,use_container_width=True,hide_index=True)

elif st.session_state.nav=='Seguiment del projecte':
 section('Seguiment del projecte','Calendari, Work Packages, lliurables, fites i tasques calculats a la data seleccionada.')
 c=st.columns(4)
 with c[0]: card('Progrés planificat',pct(K['plan']),'Percentatge ponderat que hauria d’estar completat segons calendari.')
 with c[1]: card('Progrés real',pct(K['real']),'Percentatge ponderat efectivament completat a la data d’anàlisi.')
 with c[2]: card('Lliurables vençuts',K['overdue'],'Lliurables amb data prevista superada i sense finalització registrada.')
 with c[3]: card('Hores planificades',int(pd.to_numeric(filtered('Tasks',pid).Hores_planificades).sum()),'Càrrega total planificada de les tasques del projecte.')
 tabs=st.tabs(['WorkPackages','Deliverables','Milestones','Tasks','Economics'])
 for tab,n in zip(tabs,['WorkPackages','Deliverables','Milestones','Tasks','Economics']):
  with tab: st.dataframe(filtered(n,pid),use_container_width=True,hide_index=True)

elif st.session_state.nav=='Resultats en startups':
 section('Resultats en startups','Seguiment individual de capacitats, mercat, inversió, ocupació i retorn territorial.')
 df=filtered('Startups',pid); st.dataframe(df,use_container_width=True,hide_index=True)

elif st.session_state.nav=='Analítica predictiva':
 section('Analítica predictiva','Models de priorització i escenaris de risc. En aquesta fase són models explicables basats en regles i tendències; no es presenten com a probabilitats de machine learning.')
 # multiple explainable predictive models
 models=[('Risc de calendari',min(100,round(100*min(max(K['plan']-K['real'],0)/.25,1))), 'Desviació entre trajectòria planificada i real.'),('Pressió pressupostària',min(100,round(100*max(0,K['committed']/max(K['budget_plan'],1)-.70)/.30)), 'Compromisos acumulats respecte del pressupost disponible.'),('Risc documental',min(100,K['docs']*20),'Evidències o justificants pendents que poden comprometre el tancament.'),('Risc de governança',min(100,K['openr']*22),'Riscos oberts i necessitat d’accions correctores.'),('Risc d’objectius',0,'Distància dels objectius clau respecte dels seus targets.')]
 o=filtered('Objectius',pid); ratios=[]
 for _,r in o.iterrows(): ratios.append(float(r.Valor_actual)/max(float(r.Valor_objectiu),1))
 models[-1]=(models[-1][0],round(100*(1-min(ratios))) if ratios else 0,models[-1][2])
 cols=st.columns(len(models))
 for i,(n,v,d) in enumerate(models):
  with cols[i]: card(n,f'{v}/100',d)
 section('Causes i accions correctores','Priorització dels riscos oberts, responsables i resposta prevista.')
 rr=filtered('Riscos',pid); st.dataframe(rr,use_container_width=True,hide_index=True)
 st.markdown('<div class="call"><b>Evolució futura:</b> amb històric suficient es poden incorporar models de supervivència/retard, regressió per desviació pressupostària, classificació de risc documental, forecasting de resultats i models de propensió per startups, sempre amb validació, explicabilitat i supervisió humana.</div>',unsafe_allow_html=True)

elif st.session_state.nav=='Data Hub':
 section('Data Hub','Les taules són la font del sistema. Visualitza-les, descarrega-les o carrega un Excel/CSV per substituir dades durant la sessió.')
 st.markdown('### Visualització de taules')
 name=st.selectbox('Taula de dades',TABLES,index=0); df=D[name]
 st.dataframe(df,use_container_width=True,hide_index=True,height=440)
 st.download_button(f'Descarregar {name}.csv',df.to_csv(index=False).encode('utf-8-sig'),file_name=f'{name}.csv',mime='text/csv',use_container_width=True)
 st.markdown('### Carrega de dades')
 up=st.file_uploader('Carrega un Excel (.xlsx) amb fulls homònims o un CSV per actualitzar la taula seleccionada',type=['xlsx','csv'])
 if up:
  try:
   if up.name.lower().endswith('.csv'): st.session_state.dades[name]=pd.read_csv(up)
   else:
    x=pd.ExcelFile(up)
    for sh in x.sheet_names:
     if sh in TABLES: st.session_state.dades[sh]=pd.read_excel(up,sheet_name=sh)
   st.session_state.mode='DADES CARREGADES · SESSIÓ'; st.success('Dades carregades.'); st.rerun()
  except Exception as e: st.error(f'No s’han pogut carregar les dades: {e}')
 if st.button('Restablir dades fictícies'): st.session_state.dades=load_demo(); st.session_state.mode='DEMO · DADES FICTÍCIES'; st.rerun()

elif st.session_state.nav=='Metodologia':
 section('Metodologia','Regles de càlcul, governança, traçabilitat i límits interpretatius.')
 st.markdown('''<div class="call"><b>Cadena de valor:</b> Inputs → Activitats → Outputs → Outcomes → Impactes → Retorn territorial.<br><br><b>Execució temporal:</b> el progrés es calcula a partir de lliurables ponderats i dates previstes/reals; no s’introdueix manualment.<br><br><b>Early warning:</b> els scores són índexs de priorització explicables, no probabilitats. La decisió final correspon a l’equip responsable.<br><br><b>Traçabilitat:</b> les dades públiques verificades s’identifiquen a Projectes; la resta del prototip és fictícia amb finalitat demostrativa.</div>''',unsafe_allow_html=True)
 st.markdown('### Fonts públiques utilitzades')
 for _,r in D['Projectes'].iterrows(): st.markdown(f"**{r.Nom_projecte}:** {r.Font_publica}")
