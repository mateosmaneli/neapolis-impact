import streamlit as st, pandas as pd, numpy as np, plotly.graph_objects as go
from pathlib import Path
from datetime import date
import io
st.set_page_config(page_title='NEÀPOLIS IMPACT',page_icon='◉',layout='wide',initial_sidebar_state='collapsed')
BASE=Path(__file__).parent/'dades'
TABLES=['Projectes','Inputs','Activitats','Objectius','Outputs','Outcomes','Impactes','Hipòtesis','Retorn territorial','WorkPackages','Deliverables','Milestones','Tasks','Economics','Startups','Riscos','Històric_projectes']
EMBEDDED_DATA = {
    'Projectes': 'eNrFlL1uIzcQx/sAeYeBqgSgvj8vqhx5HRxw8RkX+VIuKO5InmSX3JBcybrKyCukSndXXZOr0l2KFPsmfoG8Qoa70lo28tEESCNwR0POf/6/If/47ffnSZxb8x0qj+LSZA8fS8oL9/AZaU9e+jilBO3Dl1EyFeVdtiIfe7SWvLHEoXPpZUyaFNXLNYnIhR3Ngc2mrHzrSYkrazZWZiFVS12+lxlqz1F0rsiN8/GttLcyNvHacJylrizGzihyHFuhxjUXk5acuOAD0iBPXHBqnBerlJTkLazDW8lHr6j6/9NPrnp9sZAZdwrJ/d3PUZZbPikJPcA5OVvknopGGuSUGl9l4mkmaW22ktdcBMu3uUnJQReWUieo9UmMmthrSmXYxKFUwleYelt+FIPeYNzuTdqsqlr2B+3e6NjPG24o+puy37xcwP3dT3BQitwOQvDNepApfzjUW5MWeeUq1NguDUhlMQlWgDIZcIMHOnAdiQkwMOuL3MFnnKSo/BWCqs9F68LYTIaAgHBeUCNgyyKTJmoVy2WJW7Qu7CQ4x8zAudy3xI33ufui293tdh2NsvKmw/ldVaFon5rbTg4YtrJdeZLwMe1E7rvia/Qykdwb5OVHZvxDgW4OdYTb36DzoXKCaejLG0858JD48oMidJ1Af8Bw/M7Y70ff8o+4fvXl2WIJSyu1W6OFw5/icl9+sLjZ35Tv3khYkN/DjvwNLEyhef2KNjfe/TVTnoOGv4gKa3LJoX/A3+8f8M+YfXvY47sGeIuqqJxtvVQMsTbZyzTAJEBltMl4IiqurWMbz1+L1uRZrzOeTsW4D/c//gLVHZrDeDjrTGYTMX1WRa+jlphCdZcAg0QsnDiaQJYrsM85DwOwlS9CDeBBTM2+GiYehiKbw8Yw6vrmQlaknqTiwZiDOQrmY2rFDf/Crjipg0VX10a742JU2f4AmHFW0oFrEDMMwSPqqulHxJ9AHorFaHn2IrpcHp05U56MhiuGoElv/gfOwyfXfNg/veZn/Eypg2cWPWpVD/LBwDk8fn74XeIrf4p9Npp2hrOZGE0fYZ9OO6MBR8cN9n7vKfdIGUeOn2W2di23/LqsUl7KuqbD8Io1D0POl0Sy2MLiUSrPy79jVqNDzn+C+E+vTYF6',
    'Inputs': 'eNrFVs1yG0UQvvMUUzm3HGkl2c7RyEpKVUEYR4bcVK3ZtjKwO7OZH2PnlNfgBie4UBy4cdWb8CT0zK7+SAkUpJg97Nb09k5/+3V/3TPKp5U135L0BGNTrhejfKp0FTyM0n2iquAay5U1d7T4LTd2aqbGqjlp+Cqg9sqjhxudHkMX75focZorVxmtZqpIb8aGbd7i4mdsTJ9dtTswwJJDiPzP9z8My8qSJg6gUFwqZ0PlVYARez1XGjV/WZL2olr8MSuU3DLCqy8H4qmwJIN1xonCSCwcPGvzddKG4c01XDZ4CoKsnfVb7dNW2ll6JZV4y38itBE5WXWH/BC3Zh0L98aawfBtUJXwi1+kVlKMafFjZQrlhBIT1DlpDddLlG9CidrB2ufpyueUUVfEXprcI0Hvwmu092mDSKmxDr5IT4UwlMYp56lEQavvoZMxyqXv44DsQXrlKBKq9F2kiIOv8X0A1SHvUUDnnLEaO0cu1HcoldGPBbnPqqhQ1YBvLZLzNkgfLLLKtterSoAOo6X1Tx2KNOOt/ffGftf7hm8faurm+vOLwUSMvt5W1c2QS7J+B/3u+en56cnZs6gmwW/uY7X8DVmEdSCyDF4ZyWxRsKai4JqqrJcIDZoz5sdFv+MD6DYxxMvYRMQLa0IFL7j52ZqZurnARV4qzemxXEyL31tNrbUoD7K2RHgUW18qPeR+6T8B2h7UMLn8CvOQkvnc2FDCgFuHuqdkYZDa3fKmMe74YfGrpfnDm8VP7zAVWkne5KYwc/UJ8tnfUqQ02pQskFmBd5tahStj/YrEW2PLmsSKnMQW93WyEiHrH4/JLgx6k4uXw/Hkv8nh7KyXnZ/0+v8kh+5HC3UL1X5S6LR3aOHA6HvqYCO7HgumaZlFyLJd2ToQWQ+eDEysMaXnwE1VhlmqFu6wUgWWnPDcVGeUP9ndYTmTtS90GaVXVap/OjLSPlykqaA50JxqHeo0fZi5DYU2mV19Gce/t2aG+REQ7TOm2Ks1Gr/uxINcHKrxgBYn1lJ5m91kZRVYxRA57jh+9f6fkdv8S5ZIpaV8yC3XSmChUEvaffS6T57HHrtsOITkzfbzr9Qe3LkbsPuw2GDaSdxBzZkXj0baQWpvgB6DsI/F8RdGZdkD',
    'Activitats': 'eNq1ls1y2jAQx+99Cj2AmOAPiHN0gWQyk2YyE9L2xiiyIGptySPJNOmpr9Fbb+29j8Cb9Em6ko3tFEpiEi7MWpZXP3b/u6vzZJYr+YlRw/ClzJqH82RGqOFLbojBcW1NeV7o1ptTLkjqrDExZMYFp7w05xycsSXXhuD3JJVqJm+ta17gG+G+KFeJ1hI84AlsNG+u+h4ekQwOQcmfb98nGfgQLJGKEzTmWhW5dRDDrmuWMkr56jfiKOFkIaSGk9fGGXyliEIAkKx+CQqfc0SWRKx+2lWBUoKmyQj7fX/Q6w974HBtBn08xACjTJFrMKu/+JUk5Nl4Pj6VKiMVniFpypSGL3NYMm65I+FxTeh5PW8AJtZMay6Fxl6EJwLRQuln8wX4HRMGlplGOaDJ9V9kev2GvIQQYugB4p1U4NDz/M6AIR5JIdi9DWCVix6zmzU54mJpkVWzpSPqSYPq9+AooKWlKxtOf9iZdoDHLJNoTB5AgfNCW+ojlDFFQead2EqgljnEOTf0jm0q0ceXzHyR6nP4AX5cTcRi9SPlGgqCpUhD6bGMoFRSkjp+SYu8FN8+dWKLpJSeNV2deLiuPO8pOt+mSxtuirpoBcnsfvd8c3GGzyQkVrizO4IFVUYjawYeiK8pj7CVzg2qAE+VvLW6R0YRoQXQ2GLQOHa5FtCUFqw7TdimGWJTHYL9XTAhjhOSl/3BpfDCpQ5kl8qHDFgQdJUiA2QgnTNVknSEC6tQHVuBAdwAQ89f2jLdhTbAV+AlYWWU6rNLcdl3gs857dzZbNNoUheWmspTgvstmACPwml8MbmcOpG/JZqlXLBW33fqZlRWkt9L3kEzBiBEfs8/AZTb6qwNeT9i8l9dRIFtonWT6tuya4louAsmwFBK4JhKqliVkP3qKmh3SjBtcsLW2Al3YYT4OoOxh65BHwzZC4T9ZnIP04ZbKXeWSrg5psO1dHeSVNIFhcTlfeFcGLZQ0Jn3lm1oc9KaIZCeUrbeHrcF2NWLRx+9f8rappBA7y+9OcL9637LHSd62R2novbhHrYoXEZRLqG9Q2zVkgnHGy9JWrzGbafdzqP/tylYOHgkt0zBqJmCT8zoCvAAQXtiBkbb2yk8HDxgW/pq1PTVHa2sgjtAsLZ0VwhW3V6jR0x/AUhliXM=',
    'Objectius': 'eNrNVEtu2zAU3PcURIHuGNSWYidZumkSGEgTowja7oJn6tlgKpECSalpV71GT9B00VWP4Jv0JB3Sv8T2It15I4gfvZl5M3rD4rZ29o5VYHllq/ViWNzacXzVjbxevtzouvHr/ZHT1ulAQX6g0rr1wXxJKjRUyqEptKICG6qk5sWo05WnVKGQKP5+/3FW1Y4N41iTeKu9a+oE2ZXveWLd7Cc5oagmFXG84HjdEy6XXuhUQRtjW5zP/sgzX7Oa/Z5oJbuy2+nIo2P5SvhALjS1F1SNRaVLcKPn0sjky3PULoHuREulLuZIomKnIFxo07Lz2AIbZY3he22Nf/mYSiaPOrKfbTKxtcXCRF2LysWzaeXyAtsOnBwH64wI7OBEvFaCmm8cjUuYWKFxMDOXRz3ZP9pksPgWAjR4UgB6Jq84fLHu8+FHPJ7aUJKYWlw2ZLAWpVUAK1iUIGpVU+/w4Lgjez3A0pQN3IsBEBQj4ndgZXJQUB0bzaW4TNWhv7RfK3wszq1rKoE9dDnwfZjjP+1ztDyPeJUtUINSuV2ycvlungO3NA0GBioBdLCScsA4sxU6Py6ppUfdzDuym8m13YInMfgtR1m5PD28GVyeXd3E9p06BkhjBIp57QNXJKrZLy8m1NrkkqBFqjkmemnQdpZPYoJIqQQ4HIzQ+ok2utgCRR+Do8YxysFiNtottIk7+LfSkckMOvoSRZSmRP/1WtNG0VwifrXFr5eCCUEj5CG+DlRslhjClamjHb7kUYCMjMEXQQ/fkifPCTpuHVy/+bSRQmVtjfAnWG4cFgSpOIBs4yfsZg8GimI2oYf1PccEgRLOw+xhuoxmvytH+I1xRmHKi+srS1NheBLz2tK8zf/BGZNjlbHIeTnDIsyUfUhTxPO00Sne0ao4KKOmRKSqA2OOXCyuZvKkF8fZBuGJDik23OoiqcaK0zioYOt28rGxVw3dTW9Pevco/1jsVd+2qe1Fz/4BfhMKxA==',
    'Outputs': 'eNqlUltu2zAQ/O8pdIAVKlIPNJ9BErQGAjtA7bZ/BiNtErYSqfLRFv3qNXqD/ucIvklP0qXEOLYbF3UMCRJIzg5ndmfSLHujP2LtEKa6e1xMmqX2rvcOZuPvnWi1WerrcCx9XIraedHCQkknHJwLJ5YdWm/EUB+xL64yBmei671Nmt8/fl50vUGFjTZSJOfSGt8HxtliTri3Thjne5t89pjUuutbdKiSluqkkwqNMBIqemwEAs94mTKeZgXM2AF3cXijDRIMkw6VCwhgPAPGONyFk8jM0jw7jDmHM60UfpNa2STqTDHgrXgp1Rc0VhsgVl5BvUZuGeF0HYcpuq/afCre0+ehP2jtwLu4fE1yoQAbd0J9lWYnKTsZ5T5Rz2Fu9LVoyLYzQlklaioVraWGcnDxLDJVKS/3KsnhtK4HIa2uiSBxSE5DcQkMxHi2JSkQUWeK+enlxXQe7eyXU23JocZkKStHYzss/LEpUUsTolMbJLrVPbAivJttKoOmh6nusOVw1YphwsHg6j6ZKIe3huLN6OlbsZ5TkJP/ZywIlc4WH9hmMtAb3SN5v9GmE61036NbYPm+XLDD7uMwUYF9jLnFWy9D1hM59vsGzeqXqofgwyuQEftX8HfmTxvHmPlXSCP183Vv5XZjtLQ4cgBP5i/SHtPndRT/AAoC1PE=',
    'Outcomes': 'eNqtU0uO00AQ3XOK3rCrCLcdJ5PlKJNFJEgQTIBdVGn3RA1td9OfgFhxDXbcYY4wN+EkVNsezSQTQVCwZLfbLr/36tXzvFpbZz5KESQsTP2wmVdrE4MwtYRlv75DbdzabFKBiv0WRYioYdWogAGuMOC6lj46bBH62mevMw5TrG30rPr1/cestk42sjJOIbtS3kWbEJdTKnsb0IVoPcN6w2pTSc12qFVF6BcZjHN4DnmWlwOeD7IhLPnp2Pk+dmPoC6GVbIJnhlmlTfAwKqG8OODIT+coYN7spPPq7pZZp3ZYITWxUVqFb3QPvMzSAZx362z1JlGNBtloUGQdVQ4LGb4Y92n4ni6dK5fbVqY2ArVnn6NkwhgrSQVzUkRHN6GmM3lUlp1+Ap0M+KTz6CloDjMt6xa2kkwj25gGSfTdTxqZQEZyLc3UA0mF4hDzuNACltaQxW0ayFURLQpFuNq/uDGuxqB2klw3TUPBwEp6oK55Du2Tr1Tp91gKYilgOry+fDlbXPdWiIToSam06BIGIyOYqm3XDhHe3baiJ4/DwsvOiH24/N7ZNm1KU6STs65STYczLmHM/wqTxq6E6tsjOwNqgmX0d6QMyNQV8BGoh6o9xFMTRlWD5eoDmRC3qdd+cl0WWsFM3siWlNFrJxm27aU2nsSa/xtpDq9af/CeFNNsac5pv5U+JHbFvNxG1UWxhNHkyK90EBt6cHZPf4p6j3+O/L3UP5o8bf7POI6kqsc+2/UO+je0deiv',
    'Impactes': 'eNqtUktu2zAQ3fcU3HQ3Rizarr01HBcwULtZuJ+dMCanxqSSqJJU62Wv0Ru0i6x6BN+kJ8lQUlIgBeIUzkb8aPjevDdvZfPau2sykWDjyr+Hlc25rLHd9ut7LJzP3S4VcNMf5U+DBbyrOGKES4yYlxQaj7Dlugk5fWV7/FkZxhdXwwwWWMqtsn++/1iWtaeKrPOM6pKDb+oEu1qnuremEVI+/lZoLRt2FRZqL+UeLYIeQTaF19sl6KF+Ncj0YDiGhaui512TXv0Hl4aFJz5QSVVUuPe0x6gsqU9JmW97gNEQdAYvH2HTsKH4zfnP4w/y6UWsuRCLUNXkDe0aiwnXOOctV524whkxbzaE8ayDnwn2QOhOw+tUU9FBrAnK3dk1iFgkIUIZOETZBoGFKWDBWBkKj5CMYDHezt8sN9u+/wUmUJlr12frJEaPjacLTwLOXnV8ScJ03EmYJIdG2Ql0DXNj2t5X8yvFlXG+Fq8sBSWGueJ4E/lLQ+FCErn3KJmCrNXRvbofxb9ETxm8VA1W648ZLI1rfSqx11gefwWZkThrknBWngIX3GucTOF4U1k6nBm8nl/DGq+dV+be6DuLTRuPxC42t3uJTu/1dAITfbqPB5mRi/MlPy2ePdXzqDsdVjmcr+x0anuaZ5zZQ7pbrcj1bg==',
    'Hipòtesis': 'eNrFk89OGzEQxu99inkAIyCQ3hGNRKQQIZH+uUUTe0IHvPbK40059jV6663lWh5h36RP0vGm+QNUVaS2VFlFttf2fPP7vh26aZ3iNdlMZhyrzWTopu+5br9lEjZn69Fp4syWM2ZzkeIMZ+zLZHo47ZthVaMe7cbnZDGwVDRdUOI5W7Tc3puB6OYXFweH5hSruhFw3z9+GlR1okAuJkZ4xZKaOnNjznTXCKGikLs3iaSOARACWRIpZUUX0Ys58RnNsf4uMbPM0ZZiwECL6JtuPDnYmxyZN+jZoUOoMVlGX+7eWU3PjEjAxhDolmMQWM60v0x8SwH0iXVMuQmdNnPO+RpDEdY3l3TVcCkHL/cPe9qURDGDALJaVxk9M6b8Iaab47f61/U/8ALKNCaBCkNWXaFoLxbUHVHQezKHq8bhkkJfy50oHcnt16A9KgUbtaVY8S4lewX5LAZFlNrPVgshtHcCOWGQuVo586QWkDauN+pWjwtc8e+XTCwUC8OcyM3Q3jwueGROjycno8F40vX3OpSrilqqEDQcSq+GuUJUZ3N7t49auIGMXo9vygyDU2GuYHG0evu7SkvvSi6KcTZazY3TFWnvNVEiTVUaE/DRLlOxZZ5etAGordVeUfxJlHTX3tnw3U93r/TglrseHxnsGkWfIccM5MGyVQOcjtZf6prKJmMK5cElf0Htk/SrbkodRNqSr3MNzp10EuccMLRfsFqbd/RAJsKOn4IuPDexnQQ9L5StROvkPwN5KuYfw/hlhH8A+qBz4w==',
    'Retorn territorial': 'eNqtU0tu2zAQ3fcUPMAY1scJ4qURq4CBwg0Mp+3OGNOTgC1FCiSlZtlr9AbdddEj+CY9SYeS7MSJjaZNtKBAcvjem8fH2WZVOfuZZCCY2/J+MtusHAXrDExVScar7S+YmY2SuLFut/UBNU/sOh5RdT9FGWrUcG1UwABTDLgqydcO31wlKVxiWdVebH5/+16UlSNDjKdQTJV3dRVRFksuey/rCiWTCiUCajKB5fE5ra3k0ySCozVqLRplZK0xeIFaBHJOsTIF6RmkKbxdFpAl2fkgzQbJ6Pn8GRTSGlsqhCn5ijwOeR4ct9aJwnIt2KqGtj/5OMuyErVn1oQ/Zr6Iv+J68V/sORttbNMywZXSNsSOPZnGanblSasJXEDVlh3SZTCn8NW6L6OPPHS+cl9e+UAlwkQrNJJ24gU3pxpiDLZuBNjvdpDJeJCOj0Jmx67q0hpDd8oa368MbGVdqNtI7N3K2akM5L72b1R5xCV1R2XkmNzy6MWNdSVjDpVhRySaRnkYJZClgG3BIShDjJaTd8V8eTJmM6OkwtaK9p4wXnssGXLoybSXkrHyc1D3lZHlLBqfp09Ysoemz23E3ZkrrJCWc8BJ87Z1Pup+4PwpzEdWsL7odfss0PgbctsfrBTbZ5ADdvuHgM8JI1cNFsWnFJadN91PsCUUWDuPytzW4TCP0ZwcKnKeJfp/fwE9aXY0q3uamNjIEQviNXOn40ehPfEOeOF1mjqR1B7/5fqPhJYnr6H9aKx67Jfq3mH/AVBNKEs=',
    'WorkPackages': 'eNqNkj9uwjAUh/dKvUMO8CL5H4GOFaCqUoUyIDEiNxjkltiR7VDGXqMnaPeOHTpwk16gV6iTkACKSliSX+z4e36f3u/X9/1inhn9JBInYKLTw4ffmMXlkn+NuONzqWQiq7iU/kexkdZxiI2wNs+0dcWfsTBWK2HnfjXTyvLHtbDXVzHCMORplttg8fP6Nk79cSUW2kgejKQ1eeZkDrMYw52wTu4+Axms9EYYxdXunQNBpBeiKPSYKvZD3AfCEEJALscTGEm+UtpKz8/WXMmlTHji651gy3gTIgIUFRXo5RUojLciyZOqBbHNhJGpUO64SEkuI0YhHgCNiiL48iIMpoYruxRm96ESvykDx1XCi0LH4CqSEDFgpFFFYCLcizbPbOYfXdIx3kuPCv84Ajb4n3Teb03wse+hIUXQY43fFqxTZQ2p4k2IexChRmWL12WtZvg48MoKchQ1vVIYsuntw3gyPW+MHsaUFfcj9Nj9CeW8rfp0FcubVeppC9Rpih1a8/NXjODePG6xumerOl/PFsV76b6/P+kNVs4=',
    'Deliverables': 'eNqtl0+K2zAUxveF3sEHkAf9858syziUwhBCCWQ5qI5mUOvYxnams+w1eoJ230UXXRQ6N+kFeoVKTsbKoBhLwpvwhTj5feg9fe/l36/f73a3dVN95HnHwara6zfyg+1avRaFODTsQ3H8XL/LWMfk4/xBtB07vms4K8Cat7c1b3JeduA9b+uqbPvnl/Kx7vWrNUTgmu3rQxvs/n75utzLnyj5rmoECzLRNoe6EwewXSOQoSsEbp55AQr+/Aze8rYTTz8CEdxXD7wpWfn0jQEMcRTCOESLQWIICLki5NxCoH71utrXBXe3gs+s4CkrSQiplvHMVsiZFTJtBSWDnPNUMMiwWaBMsPuyaoX0UhesFHciZ7n0drKQ6oNJxw4Ge7sxajTpZuiYNMR4ZjdGmSbcLEKItZzxbAjIiFmp5SPPD/mxbfijvLFiL6/sS0OyXwZJLhoi3oaMYk0aQjCEkZaLmQ0Z9bIxhNJBznlCFGTULNmmYWV7x5un72UuvyCCjpU5U6ZOJpA+IDR2QNTbj1ExCz/PHaRkNLMfo2CTfvAQP0piGz8YrHj3uWo+0a18cR9McQhRSOBJSiqyieDLVPsZJFE0RETL2J9qP27ifgjHg7QbNwbVfbLEKqFQpGVqk56XwU5DJO4bOwEjuDUvd7L7xmFOMyI5tZIHzGsESF6k+nUk1iZ5rgmf9NsK8ea5Bnhy6hoPnk8+Jyp0xnB0GucYv6lKGxx74xzTVW12o835AicHIt28uVmuNu5pSvrdiGhplWsm0T5JibrhxxW6lxj5Ee1TlKprjomWqTPRPUGpKh+OB0mgTYKaUKf0pP2Fh1pGflCnFKV6VhwlcYZ6pSntr386SLt10eS6782QnK7MUSI/rvt6rKbHQsvUmeu3Bau/dUj/ybTagk2s+7IL1YY7SOqH9dlpCTqXk9j/P+jW/g==',
    'Milestones': 'eNqlljFu2zAUhvcCuQMPQBYkRUnOGMROECA2jMKAx4KV6ICNTQminGbsNXqCdu/QoUOB+ia9QK9Q0nGRJyiRRHsRfoGyvt9P7+fj35+/bvL3ZVV8VFmt8KzYPN+4heXcX1e6lvulvRjLWrqH1IO2/+8qJdf4nbJlYaz8sFZ44pbqszdzyvCl3JRbi/I/n79MNu5nRuVFpSUaa1tty1pv8XLO8JS9ZfjKvR4x9PsHula21rvvSKO74kFVRprdV4k55TGhCeECSsBF/lUX1hZrnctAPH/C8z58SlgK5el4jqe88e/HWt6ZwmrHL9fS6JXOZOb8HLAjQs+hbDrgxzqABehxcE4oh/J0BxGeRo0aTB5Vts2ePoJ6LFWlN8rUTRM8hrJpIjrWBCxDrwlGCRtBeboJgaeiUYlFJY1dqWr3zWTuWY1qaTLpjRzAzLGhbHoQx3qAhej1wAkVUHZ54Him6k9FdS+W7hIU/8R1G+Ecyq78vUwalPTE7y4sgTKIFBTqxHcPHeFWkObK5K7IrxOGhjYllJGIhhFCQ+kgsd+RWynohQSELvVxZ3EYJDBUI18tmuJWG/cyhofGMcQLX6TBiPClWFzcTmaLoJRE+x0xhbKrd9uUQQkRvkg8gnIwJSgdYt9WFMqugdMGDQ2JOLQWkINBRwwwt1kzKLtmR5sVNKdo/HxmiNtnhg5W8DjyJwIBZdcoaKMCp07EoHwd9Q9VvpNn',
    'Tasks': 'eNqdmE9u3DYUxvcFcgcdgFOIf/RvWcSDJEBgGIUBLw1WQwdqPJIgadIse42eoN130UUXBeqb9AK5QkmKIiVLIz1qM/hmxp73E/VR7+P79vc/H06PdVP9LPJOoNvq7N7ILx7u1GvH25zr73p1wzv+WJRFXsg/Fl+KtjOfPS180Aj+jN5XjWgf62deFk9Fzk+iRXeiaatSfiq/qauy5T89y09/dG/kTxVlXtTy329ELcrTyx/yLUdH+evdm+/uQoze8nN9aYPTf7/+djzLyqU4VU3Bg5uibS51V1zQwx1G9/h7+aLIAxz8+1fwTrRd8fJnUASfqi+iKXn58jtHJCTRIYwPIbUSh2MZRYiM+QL12+htda6fRcdP3BOJGCSyjYSZlQQ7SVASLiDpy92NRQ0W3cYisZGJWzQpCUqjZSyyH4sZLLaFJQESK+3CaYnDK8tFd3HJG0imxrop+KeyagsJZq2eS1AHkVk5WjwppbfoKzKC9lNNvLVJRQdPpW7tpEyVveZU+qJ3k03stUGWHrAjw6mTiXLYIhnZTzZx2CYZoVbScCyVyRbR9plMrhedmuz4VeSXvLe/+FqLpjiLshvTZYeQWWmXUEvpM/wKjqL9YBOfQcBwZKV8fFlJldXmYPrSd8NNrAaBI8b8OLQLqCRVbluEI/vhJm7bhFMYqZXDIvZSGW6Rbp/hJBibGu6+4WX7JJq+/UrEjpc5V4QWg4ROJmO50DMZ2s818dsmFz6E2MnUyWypcZoL3802sRuADRMnMyfTpe5pLn4328RtADYy2J+4JdRyqYWaq5/CEXQrul+q5jN7kC++MWy8POSA47GExLDl6rDEJRPg4BYpiXmA9hKeuJYJYOFKZdBDGBnJHAxT/RkarpYJYDlK1orMnY91JmZjCc5RMwS/yKTr9c+T2OWUQUIi0zIAOB3FrtPHukHEaCUTHcsgvzTt9brg7BPrR3tmJFatciXxbNYFJ5tYbzFtvETtAvkwWssza4W9c0uiN1hoJFU7/Upa2Szrk0oSt8ESZXq5xVeyyGZpn8yRuJ2V6HNLilaSxmZpn0SRuO2U6LxI0VqOWKvtmxcSs5G0lDaXkflKStis6pEGErONekmGnXwlA2xW9uj1qdlIvSTqAL/S4Tcre3TyVG+jyEhmd/OV/j0qLZ/j7P6Hj8fbe7/GTfWwghiZmMseJKRxzyvDmjbV58LQyOGc0csY3LTn1WENm7qATnV2oU7CpyHz6rBmTXU20zuKabPhsQQ360l5v0bNlLH7ERDTpgvHEtKo58XBTZrpJzgxMjL3oZcZeIQxBwB3a12KDoueuFuhGgp4UjEHALdtXYpkRmbuTmgJHkhMCLz7N3PPdeaOXoOEzB3m9X0aOXPnFqY2BA2dxODxwpzBc4qA3VyD2LNwqBsOdIowZ/AbFshdZxmYY9ASPCyYQPjPBOSOIG54TqKxhMwE5uW9jv6297ye1UmDQI/+cwSvE/5o2KVGIXg8K4Ge8OcIvgd5TN3RORtL4EH+f5OIFsk=',
    'Economics': 'eNrFmE2O2zYUx/cFegcfgDb4/bEMJg4QoB0YbdpZGqrMDJjakiHJbpe9Rm+Qdbvsoou5SS/QK/SJlCtrJNmjyEpgwKSlGfEnvj/f+5P//vX32816n6UfbFxYdJ/u6h9w42FVfu/So9vZpEB3UWEf08xF643N9zaP0CqzeX7Yp3mx3m+jxL13cVSgt7t9mhXrON3Bw3ZPH/PTlX30CLe/TRO7idDrqIjWLnGxW9utfXQ/ua0r4La//v7ZxTdRXByyaJ2uPxzywo8DQMuj2zx9TGIggvvu6P90efZ/8Db26PIiglcroq+/WmECb7HbH/LZ5p/ffl8CoAWY8p1mr12eHfaFO6CHFUFLsiBoZbM8TaItIlhjvMDQUlm2hjOzoGj5w3eIYirmWM7hyaGr5kQhAp9Xs6PNPGo2y2HiknwWp8kxhSl6+gNGRG8cQMduIBZF39vsaF0+s78WNktyJLGHEyo0lHNovggbQz+6qHi0+czNMntIHDwYMem5GKe+IVwu+EU8PBUeR3fpDqjiKHZPfwJjtC1AwUMJ8SQTCHKiDc0xETRHNRVlS5QxjcB6mNA1c0wnCqznaotOBTpFPJwUQnwptk7R8YDHqSq5mGHsCh6eCq9PdAMJpxEdQ0vWEJ2kQXSCGd9yIvRCn3F5GN8leE70RIH1XG3RmZDptBBee1rKxpx9RrZO0QkeMjBhPrKKmIW8iIenwusT3UDCaUQHuZU3RKdNEJ0yPosQKYg+5wowoUvnmE8UWM/VFh3BYaUa41eqIUqdq+5zwnWqTrIQU6NLPFga8tyadODhqfD6VDeQcKjqKLq3xS9p9jN/gK8O+0aJrLIa8RW+LKWsITBSlXhZVnsiB8ewG6FDS7TKYGEdQtmkDS1Nw9EpGxUyvcAch/pDGkFpk+AbkPQpZCDMaIU8N1uUsyoFYeJbRqWq695pXOgqQJkzPD4yPb7qZPsMDzWOKVIrZDKOToVoEoIilS8WnNJ6zXSS4BuQ9ClkIMxohTx3RlSFlft/seKKn63d07iha+ZEjI9MjwkioiKp6pIm3qpNDdIpkcqQVQmeG8KvkOAbkPRJZCDMaIk89zHUhB04xSqYZwmFp85jp3Ghq6HM3WTx9lkWWe0dSXDKMDOmMRfTgHRLJKwXabzlBAMq6s11Jwm+AUmvRIbBDJUIQ3f83atvlvfvug6RLttcVh808FKslA2OSnv4gW52EobBprWTAo+k+BRv2gEyShEt11H5UopF8KVaK10L8jRm6H5SKm8P3+9JCeFVXeFa15qYhOKSI5Xam0BJDa0dWCcFHklxxY2+FGSUJlo+o3KilGGvSEoo07UkeZ2kYL9ebtnHRaPPY1w+fJyE4pIHVdKUGAoqa2N9tCnwSIor/vOlIKM00TIWlfekQoqgDUhXjZMvP+ZpC83IuGj0mYqT7+RUhD0SIXhiikums+8UsE2BR1JcMZwvBRmmif8AMDdcyQ==',
    'Startups': 'eNrlmL1y00AQgHtmeIebFFQ7gyVLljxUIfFAZkwC2ITSsz4fcHC6E/djTMcL8AA8AVDQQAcFhd6EF+AVWFmO7YQJGCadXNj3t7e7n9a7a//89v1oNimteS64F3Bsis2ENpxH60O5XD8bj2jTWBgLayUNJOzr1xNuBXJZfYETHsrlaDLuwMm0vkmGteyRLoOfcIUBToLfHnNTiGZyVNAFfjW5K8vqsxdONtOHgjTqiT/TjapZr97qmVhMONa6PXpXa/99ke4NqMib4EhOCu0dmTQX1tUG00GPM5wMHj3ccmMt43HiLVbvcSpVfd31a/c7ERxgUQbHZj/evBsUpRVazGq72KF0NpTkO4zolODm0JAaGBnnhZarK+BUKtRmjkwyheyOUN5WXyHuxDF0YeA4KrSsMDOh6EQhLCeZfc6rj44hs4IH64yjrQXaBcJ9giy5bAy/OUclZ81D2as9Zmces1Iq4x0zjE6g5sLtwd6B0c6sBZg5858up2crF6Ig2T0YIuNGa7Got7CYMvLMSfKpQPaUnLfITGnoWesl8Q1HdpNJXbu6mmzkIOlDL4MIok79gqSONnIOFSMQ6S1WVB+8lS+DcOyJ5L76xKVwu9OP4VQs6njl2ijzVCJJeVRBv8aadJcUtoV02oUsghiidEk6vWLSXbitcKqw3IZ9aYgnpL814DPIUvpKx02I964YfALjYKUrTtipnAvNKS+uVsT5YE9JdVuY9yLI+vTljptgz66YeQoPppKKFowIryfVt6Xxgj+7PODJnvbATyHvAqWYJfv8itn34JTsWVya02PKca0h3Yd8q3r2d0Ydw7Hwr4x9kTymN6KaUfoOYvRCKuXYEKcwIGNNQewpp8//kMm7bWpWcuj1NiW0C6Omta1d3pl0DvfQHlLEsoPaPu63IpkVaKtPXhYXYjppU58SQ9bZlMvkvyD3SZVAPUZFdkLzQWrWflwez2mbOpMeZMmmSqa7oO7CQTLeHw6OxzCKOiu0Q2PK1fB84EZt6jmoz8jXZa/3zzAjGBoiRdngGbsbpjv10XGb2ooE8nhT7LJ/BhzXfyEEq2/csebVJimIrU7j4s/DFrUSOeRbtS3/O91fZvXNqg==',
    'Riscos': 'eNq9lk+O2jAUh/eVegdr1o4a/wHa5YiwGKmiCCGxRMbxjDxN4sgxdNtr9Abdd9lFF3OTXqBX6PPAlGmUoGFsECiKFcf5vS/yl/fn56+bfFVbc6+kU3hqysMALixn/mh1I/HcH2bWrMVaF9oJtyKrAb4pawFzH8/Hwqk7Y7XAmXBiZdbKuo3dj5yopChV5fBcNbWpGrEuFL6WUj/8WEljLTzSwORJA0u/fTNLCaxX1psG5b+/fpuUtVWVyv3qKNON3dROb/ByRvCckMdsKFfwb7Za+CX9SIpCVbmwGhkY1nD+8L2SEI/Db/x0EdOUDpJ0mMATn2dDfvGruaoLUelbLYXFSDSNvquERfbZPI22yu5moFsAc4UXvtbTisj+VWHkxmMSBXqH1FbvMyNdSVPWhXICU4ifPU3zxR4tYby/zR5WUw0Sa1FBKlWgw4s5NTYF9vRU9oMO9qOEjNrB6YXYU8+eBrPvLuF87BmwZ6eyZx3sPyQpbQdnF2LPPHsWzL67hPOx58CeR3AOSRPyvh2cX4g99+x5KPueEl7DnuKpcl+M/cyXcNhZkcZQOyER1f7Jf9T64mY0WOI9YV8OtD8gSI6G63rovzNkGEvXR+NmNFDMvWFj8ARx0XAFj+B9JyyNpeCjcTMaKNvesFE2PNiIhnt15D8IZBDLq/1AvUEpDwbaHfY1QOE18MX1x8l0sdMRC7cnO1dj3M6asUB1spj973/pwEEs3Jvcbx3Yf9Hb3HbWjAVKszdpMEmwDws3Ju/eMywuSa9LxoJJdicNJgnaYTFa0NS3z/Fb0HbWjAV3mj1JTyf5F0DN7po=',
    'Històric_projectes': 'eNqdWD2Om0cM7X0KH2AszP9PGdguAgRGEBhIKWxWKuRkV4KkdVLmAjlAupTpc4S9SU4SPpKftIZmAE+ahRYg33A45Hvk9+1mfTjuP23vz1vzYf9w/efd3fluvf/ptD1+vrvfPf9jnv943Gx/Wx93p3vzw/Z8d9ysH3bnT89/rTe77cm8254+79iSMLan09NhfzqvD/dn8/7zbvP89+M9Wa0PWwJ5PJ/M2/3D4ZfdA/2mQ3Di7ukE61ffW2fe3j0cnk6vN//+/uf7B0J73G72x93d63e70/HpQKbGWx/eOPuGjHNYefp/1UxaJeOciX7lpmAcYFJdReMBEQkPMGUSxnM0dVWMrwST6IcLJvlV/nqYSBh6KQsYT9HE/wUj0eRVxqWqaciNB0ydggkKk0ywK2eqRpMno8G9TAGMLxRSkRRTzsMUTGIYL7kBjDXOmtQmYTJfqsmlAsEUjSZOwRTNjQVMoxQXjoYqYAqmMkxEbhqlF0mqJpXJYJoWccF7UyAeUCa7VZuBkZaiKgnGR/qDOxWguCkU6ahGSfFUcAZ1XBCcn0LhEo70uMZVgqJ+pBsRysSNkvZTSigVpBdIGen1Uyj+kheHqqPXMdTicRKFuyk5xJL4RkXyUqZQuJmSxSuDrzJKGLHZKRTupei4aAkhUj+1+RtxK0X0gMtMwZF7IE4Gw60ExqWKsxRL44Z0k4mpmphM3lR2gWC4k8IUStNYEAMTcFXKqzMw0kmxcEIoyQzjTbYzzJmWVsLrOFAE7tUQjJtCkfKFUqJaEjobPZG+HiQvncQ9gDAS5xk8WqdgvJJDMODwN8zAyIudQpFWEgUgGHlrYtE4hRKVNTNQ6KWoAIk200zFZG0lEoKIhrSUYqo9SPhcerMSlaNyo5dukG5T3ExDZu2kxKXSmBwKxVLsJEpVFAcUJ0+N2WbujZreiDQpsM5mxBK5dr35sD3/uj/+HH+kPy8HOjJgRU0shS6ibtPIg2uygHbIowr/uEVquh5eRxEPua3M5C6BNVrX4zKRoWkCjZZ8DYxSUmtdD68DBnlwYcooSFLmRx7LnEW6m3kIcMLGZeQQddqMEGrLrcQOdeSwFCmPp9zCFuwYxkdkbdSEmGT2y3jOYaKKOtDzOTlCVTKNPKpKfMMEH00RxvbjW7SrgkZuNZrXcQk7cFAarjJE0E3oySPYZnRrqaiYMKEGnupE0ezwtXVOYcFAevHaaRxTuhIpjwGQBhookIU0cnhxgucNheeGNGiky6ARELsnLxX3MHi6ZaagE4I4oF0hem18RNIjrOEJDVThEVMdOWTllKoaZLlT/SCvy1CAxQcxgeI9v0Qe56kq4Xh4VO6ivAwAXYd2Wf34sXEMa9HIQVfOxIUhQloXTe/aL9NnlQOwj5FDGV5Bt8gkg2bgjiisLV2HiyrzfgeHIFfwg+pb9DdzbYDKKtoIS1UeOQg3YaHgEYRJCndwI4eoG40z3vFQWKFkdsB+i4BSVyc0aWEyS6aEwTMsWslN6j1TU4PDKK2LLMaAd2ii9hxTHaepakwe4oUFGjsMHTFMU1Omibg1j6B8C2G/YN7Gj9989/7Dxy++XeC2wanaSzv4nrXIHOLwhfW4ard1rZfd34lgVeYNtF64sV7kDckWmveKLTvfjbXXYmD5dNyUhcfcnrHQEGtt5H0HkhMlhzfG8UJy3vMSkESfusZJ+yrDOLHuM4XannFWIuGZCCOwBUH7fszlul1lnigSDS204ZSesehX5B2X3gbJRhTdkF9IF3ouCYnHrrHu4brKYDClvkNx9d5EJQtXYz3h1XJ0v4taaTd7Fp9uGBel4tEYYVgZS0RHboyXJQNDG8UCabh+ubqxDgqtm6O7rFm2Zx2v477svJknw9y540Wb+INM5aVJpsLSacVFmDJvwugwHkQWJbsxLle65S810D0L6G5K6kuuxZIdZEsJPWMuEIwm8tWER2YsAL04lD8gWNxamQuEdKOXDymQbJdxHuUXMJ/2Uu0WfaggPupu6Bzo/hZ5UZ/sRH0EmeXL9oy9Gnv50IrceXbuGS/fSgIme8wKYJtFp26sozZiA/kmsWby9T3rpLXH3M4fQJyQu+tZi9gwL+JLlsP4lbFCdCNZlMbiYTAUQdCG2FW/wjTUNTc7TRbIdhe7XejG8YSQ5G2o0F/9B5vBIo4=',
}

@st.cache_data
def load_demo_v83(cache_version="v8.3"):
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
APP_DATA_VERSION='v8.3'
if st.session_state.get('app_data_version') != APP_DATA_VERSION:
    st.session_state.dades=load_demo_v83().copy()
    st.session_state.mode='DEMO · DADES FICTÍCIES'
    st.session_state.app_data_version=APP_DATA_VERSION
    st.session_state.nav='HOME'
if 'nav' not in st.session_state:
    st.session_state.nav='HOME'
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
def objective_card(title,subtitle,value,desc):
 st.markdown(f'''<div class="kpi"><div class="kt">{title}</div><div style="font-size:12px;color:#37566b;font-weight:700;margin-top:5px">{subtitle}</div><div class="kv">{value}</div><div class="kx">{desc}</div></div>''',unsafe_allow_html=True)
def forecast(pid):
 # Robust fallback: never depend on a stale Streamlit session for the historical table.
 h=D.get('Històric_projectes', pd.DataFrame()).copy()
 if h.empty:
  fresh=load_demo_v83()
  h=fresh.get('Històric_projectes', pd.DataFrame()).copy()
 if h.empty:
  return {'risc':50.0,'retard':0.0,'pressupost':0.0,'objectius':0.0}
 h=h[h.Id_projecte==pid].copy(); h['Data_observació']=pd.to_datetime(h['Data_observació']); h=h.sort_values('Data_observació').tail(24); x=np.arange(len(h)); xf=len(h)+3
 def pred(c):
  y=pd.to_numeric(h[c],errors='coerce').ffill().fillna(0).values; return float(np.polyval(np.polyfit(x,y,1),xf)) if len(y)>2 else float(y[-1])
 return {'risc':np.clip(pred('Índex_risc'),0,100),'retard':max(0,pred('Retard_mitjà_dies')),'pressupost':pred('Desviació_pressupost_pct'),'objectius':np.clip(pred('Compliment_objectius_pct'),0,100)}
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
 risk=min(100,max(46,round(45*min(schedule/.25,1)+20*min(overdue/4,1)+15*min(openr/4,1)+12*min(docs/5,1)+8*min(budget_pressure/.15,1))))
 status='ALT' if risk>=70 else ('MODERAT' if risk>=40 else 'CONTROLAT')
 return wp,dl,eco,r,dict(risk=risk,status=status,plan=float(wp.plan.mean()) if len(wp) else 0,real=float(wp.real.mean()) if len(wp) else 0,overdue=overdue,openr=openr,docs=docs,budget=paid/max(budget_plan,1),paid=paid,committed=committed,budget_plan=budget_plan)

st.markdown('''<style>
.stApp{background:#f4f7fb;color:#10283d}.block-container{padding-top:1.1rem;max-width:1450px}.hero{background:linear-gradient(125deg,#071b2d,#103a53 65%,#0a6672);border-radius:24px;padding:28px 34px;color:white;margin:8px 0 18px;box-shadow:0 12px 35px #0b233326}.hero h1{font-size:42px;margin:3px 0}.hero p{font-size:17px;color:#d8e8ef;margin:0}.badge{font-size:11px;font-weight:800;letter-spacing:.13em;background:#ffffff17;border:1px solid #ffffff33;padding:6px 10px;border-radius:999px}.eyebrow{font-size:11px;letter-spacing:.16em;font-weight:800;color:#74d6de;margin-top:15px}.kpi{background:white;border:1px solid #dce7ef;border-radius:18px;padding:17px 18px;min-height:145px;box-shadow:0 4px 16px #16384d0c}.kt{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:#597286;font-weight:800}.kv{font-size:28px;font-weight:850;color:#0b2c43;margin:7px 0}.kd{font-size:12px;font-weight:800;color:#0d7b86}.kx{font-size:12px;color:#667d8d;line-height:1.35;margin-top:7px}.sect{margin:25px 0 10px}.sect h2{margin:0;color:#0b2c43;font-size:23px}.sect p{margin:4px 0;color:#6b7e8c}.risk{background:#081c2d;border-radius:20px;padding:22px;color:white;min-height:218px}.lights{display:flex;gap:11px;margin:18px 0}.light{width:32px;height:32px;border-radius:50%;opacity:.18}.on{opacity:1;box-shadow:0 0 20px currentColor}.rtitle{font-size:28px;font-weight:900}.rsub{font-size:12px;color:#bdd0dd;margin-top:8px;line-height:1.45}.projectname{font-size:18px;font-weight:850;color:#fff;margin-top:8px}.navbox{background:white;border:1px solid #dce7ef;border-radius:16px;padding:15px;margin-bottom:7px}.smallnote{font-size:12px;color:#6b7e8c}.stButton>button{border-radius:12px;font-weight:750;border:1px solid #cbdde8}.stButton>button:hover{border-color:#0a7f89;color:#0a6872}.dataframe{border-radius:14px}.call{background:#eaf7f7;border-left:4px solid #0a7f89;padding:14px 16px;border-radius:10px;color:#234a5a}
</style>''',unsafe_allow_html=True)
st.markdown(f'''<div class="hero"><span class="badge">{st.session_state.mode}</span><div class="eyebrow">PROJECT & IMPACT INTELLIGENCE SYSTEM</div><h1>NEÀPOLIS IMPACT</h1><p>Control, anticipació i impacte en una sola vista: de l’execució calendaritzada a les decisions, els resultats i el retorn territorial.</p></div>''',unsafe_allow_html=True)
if st.button('⌂  Pàgina principal',use_container_width=True,key='home_top'): gohome()
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
  st.markdown(f'''<div class="risk"><div class="smallnote" style="color:#9fc1d1">PROJECTE SELECCIONAT</div><div class="projectname">{pname}</div><div class="lights"><div class="light {'on' if K['status']=='CONTROLAT' else ''}" style="background:#22c55e;color:#22c55e"></div><div class="light {'on' if K['status']=='MODERAT' else ''}" style="background:#f59e0b;color:#f59e0b"></div><div class="light {'on' if K['status']=='ALT' else ''}" style="background:#ef4444;color:#ef4444"></div></div><div class="rtitle" style="color:{color}">RISC {K['status']} · {K['risk']}/100</div><div class="rsub">Índex explicable de priorització. Integra desviació temporal, lliurables vençuts, riscos oberts, evidències pendents i pressió pressupostària.</div></div>''',unsafe_allow_html=True)
 with right:
  if startup=='Totes':
   o=filtered('Objectius',pid,asof); cols=st.columns(3)
   for i in range(3):
    if i<len(o):
     r=o.iloc[i]; val=f"{r.Valor_actual:g} / {r.Valor_objectiu:g}"; desc=f"{r.Indicador_clau}. Mesura l'avenç de l'objectiu {r.Id_objectiu}: {r.Objectiu}."
     with cols[i]: objective_card(f'Objectiu {r.Id_objectiu}',r.Objectiu,val,f"Indicador: {r.Indicador_clau}.")
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
 section('Predicció de futur','Estimacions algorítmiques a 90 dies calculades sobre 36 mesos d’històric fictici.')
 F=forecast(pid); pc=st.columns(4)
 with pc[0]: card('Risc previst a 90 dies',f"{F['risc']:.0f}/100",'Tendència estimada de risc global a partir de l’històric de gestió.')
 with pc[1]: card('Retard mitjà previst',f"{F['retard']:.0f} dies",'Estimació del retard mitjà esperat en fites i lliurables.')
 with pc[2]: card('Desviació pressupostària',f"{F['pressupost']:+.1f}%",'Forecast de desviació entre despesa/compromisos i trajectòria pressupostària.')
 with pc[3]: card('Compliment d’objectius',f"{F['objectius']:.0f}%",'Percentatge estimat d’assoliment dels objectius clau a l’horitzó de 90 dies.')
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
 quick=[('Seguiment del projecte','Calendari, WP, lliurables, fites i tasques.'),('Resultats en startups','Última mesura disponible per startup.'),('Analítica predictiva','Semàfor, causes, escenaris i accions correctores.'),('Finances','Pressupost, compromisos, pagaments, elegibilitat i evidències.'),('Data Hub','Visualitza, filtra, carrega i descarrega les taules de dades.'),('Metodologia','Regles de càlcul, governança i traçabilitat.')]
 cols=st.columns(3)
 for i,(a,b) in enumerate(quick):
  with cols[i]:
   st.markdown(f'<div class="navbox"><b>{a}</b><div class="smallnote">{b}</div></div>',unsafe_allow_html=True)
   if st.button('Obrir →',key='q'+a,use_container_width=True): goto(a)

elif st.session_state.nav in TDC:
 name=st.session_state.nav; section(name,f'Lectura gerencial de {name.lower()} per al projecte seleccionat.')
 df=filtered(name,pid,asof)
 if len(df):
  kc=st.columns(4)
  if name=='Inputs': vals=[('Inputs actius',len(df),'Recursos registrats i disponibles.'),('Finançament',money(pd.to_numeric(df.loc[df.Tipus_input.str.contains('Finanç',case=False,na=False),'Quantitat'],errors='coerce').sum()),'Recursos financers registrats.'),('Agents implicats',int(pd.to_numeric(df.loc[~df.Tipus_input.str.contains('Finanç',case=False,na=False),'Quantitat'],errors='coerce').sum()),'Volum agregat de recursos no financers.'),('Disponibilitat',f"{(df.Estat.astype(str).str.contains('Disponible',case=False).mean()*100):.0f}%",'Inputs disponibles a la data d’anàlisi.')]
  elif name=='Activitats': vals=[('Activitats',len(df),'Activitats programades.'),('Assoliment',f"{(pd.to_numeric(df.Valor_assolit).sum()/max(pd.to_numeric(df.Valor_objectiu).sum(),1)*100):.0f}%",'Execució agregada sobre objectiu.'),('En curs',int(df.Estat.astype(str).str.contains('curs',case=False).sum()),'Activitats encara obertes.'),('Finalitzades',int(df.Estat.astype(str).str.contains('final|complet',case=False,regex=True).sum()),'Activitats completades.')]
  elif name in ['Outputs','Outcomes','Impactes','Retorn territorial']: vals=[('Indicadors',len(df),'Indicadors monitorats.'),('Assoliment mitjà',f"{(pd.to_numeric(df.Valor_actual)/pd.to_numeric(df.Valor_objectiu).replace(0,np.nan)).mean()*100:.0f}%",'Mitjana de compliment dels targets.'),('Sota 80% target',int(((pd.to_numeric(df.Valor_actual)/pd.to_numeric(df.Valor_objectiu).replace(0,np.nan))<.8).sum()),'Indicadors que requereixen atenció.'),('Actualitzats',int(df['Data_mesura'].notna().sum()) if 'Data_mesura' in df else len(df),'Indicadors amb mesura registrada.')]
  else: vals=[('Hipòtesis',len(df),'Condicions causals monitorades.'),('Criticitat alta',int(df.Criticitat.astype(str).str.contains('Alta',case=False).sum()),'Hipòtesis crítiques.'),('Risc alt',int(((pd.to_numeric(df.Probabilitat_1_5)*pd.to_numeric(df.Impacte_1_5))>=16).sum()),'Probabilitat × impacte ≥16.'),('Verificades',int(df.Estat.astype(str).str.contains('verif|compl',case=False,regex=True).sum()),'Hipòtesis verificades/complertes.')]
  for i,(a,b,c) in enumerate(vals):
   with kc[i]: card(a,b,c)

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
 section('Lectura gerencial','Desviacions de calendari i càrrega de treball per Work Package.')
 fig=go.Figure(); fig.add_trace(go.Bar(name='Planificat',x=wp.Id_WP,y=wp.plan*100)); fig.add_trace(go.Bar(name='Real',x=wp.Id_WP,y=wp.real*100)); fig.update_layout(barmode='group',height=330,yaxis_title='Progrés %'); st.plotly_chart(fig,use_container_width=True)

elif st.session_state.nav=='Resultats en startups':
 section('Resultats en startups','Seguiment individual de capacitats, mercat, inversió, ocupació i retorn territorial.')
 df=filtered('Startups',pid); c=st.columns(4)
 with c[0]: card('Startups',len(df),'Startups vinculades al projecte.')
 with c[1]: card('Inversió captada',money(pd.to_numeric(df.Inversió_captada_EUR).sum()),'Capital mobilitzat per les startups.')
 with c[2]: card('Nous clients',int(pd.to_numeric(df.Nous_clients).sum()),'Nous clients registrats en seguiment.')
 with c[3]: card('Ocupació creada',int((pd.to_numeric(df.Ocupació_actual)-pd.to_numeric(df.Ocupació_T0)).sum()),'Variació neta d’ocupació respecte T0.')
 fig=go.Figure(); fig.add_trace(go.Bar(name='T0',x=df.Nom_startup,y=df['Índex_capacitats_T0'])); fig.add_trace(go.Bar(name='Actual',x=df.Nom_startup,y=df['Índex_capacitats_actual'])); fig.update_layout(barmode='group',height=350,margin=dict(l=10,r=10,t=20,b=90),yaxis_title='Índex de capacitats'); st.plotly_chart(fig,use_container_width=True)
 st.dataframe(df,use_container_width=True,hide_index=True)

elif st.session_state.nav=='Finances':
 section('Finances','Control financer orientat a les obligacions de gestió, elegibilitat, justificació i auditoria dels projectes europeus.')
 e=eco.copy(); c=st.columns(5)
 with c[0]: card('Pressupost registrat',money(K['budget_plan']),'Pressupost planificat en els moviments registrats.')
 with c[1]: card('Compromès',money(K['committed']),'Import compromès pendent o executat.')
 with c[2]: card('Pagat',money(K['paid']),'Despesa efectivament pagada.')
 with c[3]: card('Execució',pct(K['budget']),'Pagaments sobre pressupost registrat.')
 with c[4]: card('Evidències pendents',K['docs'],'Moviments amb documentació incompleta.')
 by=e.groupby('Id_WP',as_index=False)[['Pressupost_planificat','Import_compromès','Import_pagat']].sum(); fig=go.Figure();
 for col,label in [('Pressupost_planificat','Planificat'),('Import_compromès','Compromès'),('Import_pagat','Pagat')]: fig.add_trace(go.Bar(name=label,x=by.Id_WP,y=by[col]))
 fig.update_layout(barmode='group',height=360,yaxis_title='EUR'); st.plotly_chart(fig,use_container_width=True)
 st.markdown('<div class="call"><b>Controls crítics:</b> elegibilitat temporal i per categoria, traçabilitat factura-pagament-activitat, cofinançament, compromisos, desviacions, documentació justificativa, evidències de lliurables i preparació per auditoria.</div>',unsafe_allow_html=True)
 st.dataframe(e,use_container_width=True,hide_index=True)

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
 F=forecast(pid); section('Forecast a 90 dies','Models de regressió lineal entrenats sobre 36 mesos d’històric fictici per detectar tendències i anticipar desviacions.')
 fc=st.columns(4)
 with fc[0]: card('Risc futur',f"{F['risc']:.0f}/100",'Índex de risc projectat.')
 with fc[1]: card('Retard previst',f"{F['retard']:.0f} dies",'Retard mitjà projectat.')
 with fc[2]: card('Desviació pressupost',f"{F['pressupost']:+.1f}%",'Desviació pressupostària projectada.')
 with fc[3]: card('Objectius previstos',f"{F['objectius']:.0f}%",'Compliment agregat projectat.')
 h=D['Històric_projectes']; h=h[h.Id_projecte==pid].copy(); h['Data_observació']=pd.to_datetime(h.Data_observació); fig=go.Figure(); fig.add_trace(go.Scatter(x=h.Data_observació,y=h.Índex_risc,name='Risc històric',mode='lines')); fig.add_trace(go.Scatter(x=h.Data_observació,y=h.Compliment_objectius_pct,name='Compliment objectius',mode='lines')); fig.update_layout(height=340,yaxis_title='Índex / %'); st.plotly_chart(fig,use_container_width=True)
 section('Causes i accions correctores','Priorització dels riscos oberts, responsables i resposta prevista.')
 rr=filtered('Riscos',pid); st.dataframe(rr,use_container_width=True,hide_index=True)
 st.markdown('<div class="call"><b>Evolució futura:</b> amb històric suficient es poden incorporar models de supervivència/retard, regressió per desviació pressupostària, classificació de risc documental, forecasting de resultats i models de propensió per startups, sempre amb validació, explicabilitat i supervisió humana.</div>',unsafe_allow_html=True)

elif st.session_state.nav=='Data Hub':
 section('Data Hub','Les taules són la font del sistema. Visualitza-les, descarrega-les o carrega un Excel/CSV per substituir dades durant la sessió.')
 st.markdown('### Visualització de taules font i històriques')
 st.info('Selecciona una taula per inspeccionar directament les dades que alimenten els càlculs. Històric_projectes conté 36 mesos × 3 projectes = 108 observacions fictícies per a la demostració predictiva.')
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
 if st.button('Restablir dades fictícies'): st.session_state.dades=load_demo_v83(); st.session_state.mode='DEMO · DADES FICTÍCIES'; st.rerun()

elif st.session_state.nav=='Metodologia':
 section('Metodologia','Regles de càlcul, governança, traçabilitat i límits interpretatius.')
 st.markdown('''<div class="call"><b>1. Teoria del Canvi:</b> estructura Inputs → Activitats → Outputs → Outcomes → Impactes → Retorn territorial, amb hipòtesis explícites i indicadors vinculats als objectius.<br><br><b>2. Motor temporal:</b> la data d’anàlisi reconstrueix la fotografia del projecte. El progrés es calcula a partir de lliurables ponderats i dates previstes/reals; no s’introdueix manualment.<br><br><b>3. Control operatiu:</b> integra WP, tasques, fites, lliurables, càrrega de treball, riscos, responsables, pressupost, pagaments i evidències documentals.<br><br><b>4. Early warning:</b> combina desviació de calendari, venciments, riscos oberts, documentació i pressió pressupostària per prioritzar l’atenció gerencial.<br><br><b>5. Predicció:</b> la demo incorpora 36 mesos d’històric fictici i regressions de tendència a 90 dies per risc, retard, pressupost i compliment d’objectius. En producció, els models s’han de validar amb històric real, mètriques d’error, control de deriva i supervisió humana.<br><br><b>6. Finances i auditoria:</b> control d’elegibilitat, compromisos, pagaments, cofinançament, factura/justificant, evidència d’activitat i traçabilitat per WP.<br><br><b>7. Governança de dades:</b> definicions comunes, responsable de dada, periodicitat, font de verificació, baseline, target i registre de modificacions.<br><br><b>8. Escalabilitat:</b> cada projecte conserva la seva TdC i indicadors específics dins d’un model de dades comú que permet lectura de cartera.<br><br><b>9. Traçabilitat de la demo:</b> les dades públiques verificades s’identifiquen a Projectes; els valors de gestió, històrics i prediccions són ficticis i tenen finalitat demostrativa.</div>''',unsafe_allow_html=True)
 st.markdown('### Fonts públiques utilitzades')
 for _,r in D['Projectes'].iterrows(): st.markdown(f"**{r.Nom_projecte}:** {r.Font_publica}")
