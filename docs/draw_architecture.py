from pathlib import Path
import html
import cairosvg

W, H = 2540, 1420
out = []
out.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <marker id="arrow-blue" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#2563eb"/></marker>
  <marker id="arrow-green" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#059669"/></marker>
  <marker id="arrow-orange" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#ea580c"/></marker>
  <marker id="arrow-slate" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#475569"/></marker>
  <style>
    text {{ font-family: Inter, Arial, sans-serif; fill:#0f172a; }}
    .title {{ font-size:30px; font-weight:700; }}
    .subtitle {{ font-size:15px; fill:#475569; }}
    .head {{ font-size:19px; font-weight:700; }}
    .body {{ font-size:15px; }}
    .small {{ font-size:13px; fill:#475569; }}
    .tiny {{ font-size:12px; fill:#475569; }}
    .tag {{ font-size:13px; font-weight:700; }}
  </style>
</defs>
<rect width="100%" height="100%" fill="#ffffff"/>
''')

def esc(s): return html.escape(s)
def rect(x,y,w,h,fill='#f8fafc',stroke='#64748b',rx=18,sw=2,dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
def txt(x,y,lines,cls='body',anchor='middle',color=None,linegap=23):
    if isinstance(lines,str): lines=[lines]
    style = f' fill="{color}"' if color else ''
    out.append(f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}"{style}>')
    for i,line in enumerate(lines):
        out.append(f'<tspan x="{x}" dy="{0 if i==0 else linegap}">{esc(line)}</tspan>')
    out.append('</text>')
def line(points,color='#475569',width=3,marker='arrow-slate',dash=None):
    p=' '.join(f'{x},{y}' for x,y in points)
    d=f' stroke-dasharray="{dash}"' if dash else ''
    m=f' marker-end="url(#{marker})"' if marker else ''
    out.append(f'<polyline points="{p}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"{d}{m}/>')
def label(x,y,s,color='#334155'):
    w=max(110, len(s)*8.1+22)
    out.append(f'<rect x="{x-w/2}" y="{y-17}" width="{w}" height="28" rx="9" fill="#ffffff" stroke="#e2e8f0"/>')
    txt(x,y+2,s,'tiny',color=color)

# Header
txt(1270,48,'AWS Scalable Web Application','title')
txt(1270,78,'EC2-based · Multi-AZ · High Availability · Auto Scaling · CDN Caching','subtitle')

# User -> DNS -> CDN main ingress
rect(55,125,235,105,'#eff6ff','#3b82f6')
txt(172,164,['GLOBAL USERS'],'head')
txt(172,193,['Browser / Mobile clients'],'small')
rect(375,125,285,105,'#f5f3ff','#8b5cf6')
txt(517,165,['Amazon Route 53'],'head')
txt(517,194,['A / AAAA Alias → CloudFront'],'small')
rect(750,125,390,105,'#f5f3ff','#8b5cf6',sw=2.5)
txt(945,164,['Amazon CloudFront'],'head')
txt(945,193,['HTTPS · Edge locations · Cache behaviors'],'small')
line([(290,177),(375,177)],'#475569',3,'arrow-slate')
label(332,150,'DNS lookup')
line([(660,177),(750,177)],'#475569',3,'arrow-slate')
label(705,150,'Alias')

# WAF association
rect(780,265,330,82,'#fff1f2','#e11d48')
txt(945,297,['AWS WAF · CLOUDFRONT Web ACL'],'head')
txt(945,322,['Managed rules · Rate limits · OWASP-aligned'],'small')
line([(945,265),(945,230)],'#e11d48',2,'arrow-slate','7,6')
label(1085,246,'Associated protection (not inline)','#9f1239')

# S3 static origin
rect(1325,125,500,120,'#ecfdf5','#059669')
txt(1575,164,['Private Amazon S3 origin'],'head')
txt(1575,193,['Static assets · Block Public Access'],'small')
txt(1575,216,['CloudFront Origin Access Control (OAC)'],'small')
line([(1140,177),(1325,177)],'#059669',3,'arrow-green')
label(1230,150,'Static cache miss')

# VPC outer
rect(45,390,1925,965,'#ffffff','#16a34a',rx=24,sw=3)
txt(80,430,'AWS REGION · VPC 10.0.0.0/16','head','start',color='#166534')

# VPC IGW and ALB
rect(100,465,250,100,'#fff7ed','#ea580c')
txt(225,505,['Internet Gateway'],'head')
txt(225,531,['VPC attachment'],'small')
rect(520,455,1040,120,'#eff6ff','#2563eb',sw=2.5)
txt(1040,495,['Application Load Balancer (ALB)'],'head')
txt(1040,523,['Internet-facing · HTTPS :443 · Listener rules · Target health checks'],'small')
txt(1040,547,['ALB nodes enabled in Public Subnet A and Public Subnet B'],'small')
# CloudFront origin to IGW then ALB
line([(945,230),(945,365),(225,365),(225,465)],'#2563eb',3,'arrow-blue')
label(605,354,'Dynamic / API origin request · HTTPS 443')
line([(350,515),(520,515)],'#2563eb',3,'arrow-blue')

# ASG cross-AZ
rect(745,605,520,78,'#fff7ed','#ea580c',rx=15,sw=2)
txt(1005,637,['EC2 Auto Scaling Group'],'head')
txt(1005,660,['Launch Template · Target Tracking · Min 2 / Desired 2 / Max 6'],'small')

# AZ groups
rect(75,715,900,585,'#f8fdff','#0ea5e9',rx=24,sw=2,dash='10,7')
rect(1015,715,900,585,'#f8fdff','#0ea5e9',rx=24,sw=2,dash='10,7')
txt(525,750,'AVAILABILITY ZONE A','head',color='#0369a1')
txt(1465,750,'AVAILABILITY ZONE B','head',color='#0369a1')

# Public subnet cards
rect(105,775,840,120,'#ecfdf5','#16a34a',rx=15)
rect(1045,775,840,120,'#ecfdf5','#16a34a',rx=15)
txt(135,804,'PUBLIC SUBNET A · 10.0.1.0/24','tag','start',color='#166534')
txt(1075,804,'PUBLIC SUBNET B · 10.0.2.0/24','tag','start',color='#166534')
rect(135,822,330,57,'#ffffff','#86efac',rx=10,sw=1.5)
txt(300,847,['NAT Gateway A · Elastic IP'],'body')
txt(300,867,['Default route → Internet Gateway'],'tiny')
rect(1075,822,330,57,'#ffffff','#86efac',rx=10,sw=1.5)
txt(1240,847,['NAT Gateway B · Elastic IP'],'body')
txt(1240,867,['Default route → Internet Gateway'],'tiny')
txt(700,850,['ALB subnet association'],'small')
txt(1640,850,['ALB subnet association'],'small')

# App subnet cards
rect(105,925,840,150,'#e0f2fe','#0284c7',rx=15)
rect(1045,925,840,150,'#e0f2fe','#0284c7',rx=15)
txt(135,954,'PRIVATE APP SUBNET A · 10.0.11.0/24','tag','start',color='#075985')
txt(1075,954,'PRIVATE APP SUBNET B · 10.0.12.0/24','tag','start',color='#075985')
rect(270,973,510,78,'#ffffff','#38bdf8',rx=12,sw=1.5)
txt(525,1004,['EC2 Application Instance A'],'head')
txt(525,1029,['ASG-managed · Private IP only · App port 8080'],'small')
rect(1210,973,510,78,'#ffffff','#38bdf8',rx=12,sw=1.5)
txt(1465,1004,['EC2 Application Instance B'],'head')
txt(1465,1029,['ASG-managed · Private IP only · App port 8080'],'small')

# Database subnets
rect(105,1100,840,165,'#f1f5f9','#64748b',rx=15)
rect(1045,1100,840,165,'#f1f5f9','#64748b',rx=15)
txt(135,1129,'PRIVATE DB SUBNET A · 10.0.21.0/24','tag','start')
txt(1075,1129,'PRIVATE DB SUBNET B · 10.0.22.0/24','tag','start')
rect(255,1150,540,88,'#ffffff','#2563eb',rx=12,sw=1.7)
txt(525,1183,['Amazon RDS · PRIMARY'],'head')
txt(525,1210,['MySQL / PostgreSQL · Read + Write'],'small')
rect(1195,1150,540,88,'#ffffff','#64748b',rx=12,sw=1.7)
txt(1465,1183,['Amazon RDS · STANDBY'],'head')
txt(1465,1210,['Different AZ · Failover target · Not a read replica'],'small')

# Main application data and ALB paths
line([(760,575),(760,595),(525,595),(525,973)],'#2563eb',2.5,'arrow-blue','8,6')
line([(1320,575),(1320,595),(1465,595),(1465,973)],'#2563eb',2.5,'arrow-blue','8,6')
label(525,915,'Target Group · HTTP 8080')
label(1465,915,'Target Group · HTTP 8080')
# ASG dashed lines
line([(875,683),(875,704),(525,704),(525,973)],'#ea580c',2,'arrow-orange','7,6')
line([(1135,683),(1135,704),(1465,704),(1465,973)],'#ea580c',2,'arrow-orange','7,6')
# DB paths
line([(525,1051),(525,1150)],'#2563eb',2.7,'arrow-blue')
line([(1465,1051),(1465,1150)],'#2563eb',2.7,'arrow-blue')
label(525,1090,'SQL · TCP 3306 / 5432')
label(1465,1090,'SQL · TCP 3306 / 5432')
# replication
line([(795,1194),(1195,1194)],'#2563eb',3,'arrow-blue')
line([(1195,1220),(795,1220)],'#2563eb',2,'arrow-blue','6,5')
label(995,1174,'RDS-managed synchronous replication')
# NAT egress from apps to NATs
line([(270,1000),(205,1000),(205,879),(300,879)],'#059669',2.5,'arrow-green')
line([(1720,1000),(1800,1000),(1800,879),(1240,879)],'#059669',2.5,'arrow-green')
label(205,950,'Outbound only')
label(1800,950,'Outbound only')
# NAT to IGW egress dashed
line([(300,822),(300,565)],'#059669',2,'arrow-green','7,6')
line([(1240,822),(1880,822),(1880,590),(365,590),(365,515),(350,515)],'#059669',2,'arrow-green','7,6')

# ASG management note connected to two instances
# VPC service callouts in the right blank portion inside VPC
rect(1610,465,315,105,'#f5f3ff','#8b5cf6')
txt(1767,498,['Systems Manager VPC Endpoints'],'head')
txt(1767,525,['ssm · ssmmessages'],'small')
txt(1767,547,['SSM Agent traffic · HTTPS 443'],'small')
line([(1610,520),(1570,520)],'#8b5cf6',2,'arrow-slate','7,6')

# Add a small VPC data-path note
rect(1615,605,300,78,'#fffbeb','#d97706',rx=12)
txt(1765,637,['Network controls'],'head')
txt(1765,661,['SG references · DB private · NACLs'],'small')

# External administration and monitoring side
rect(2010,375,470,105,'#f5f3ff','#8b5cf6')
txt(2245,415,['Administrator'],'head')
txt(2245,444,['IAM role / Identity Center · least privilege'],'small')
rect(2010,520,470,105,'#f5f3ff','#8b5cf6')
txt(2245,560,['AWS Systems Manager'],'head')
txt(2245,589,['Session Manager · Run Command · Parameter Store'],'small')
line([(2245,480),(2245,520)],'#8b5cf6',2.5,'arrow-slate')
line([(2010,573),(1950,573),(1950,520),(1925,520)],'#8b5cf6',2,'arrow-slate','7,6')
label(1985,548,'PrivateLink · HTTPS 443')

rect(2010,735,470,135,'#fff7ed','#ea580c')
txt(2245,777,['Amazon CloudWatch'],'head')
txt(2245,806,['AWS service metrics · EC2 Agent logs'],'small')
txt(2245,832,['Dashboards · Alarms · Logs Insights'],'small')
rect(2010,920,470,105,'#fff1f2','#e11d48')
txt(2245,960,['Amazon SNS'],'head')
txt(2245,989,['Email · SMS · HTTPS notifications'],'small')
rect(2110,1080,270,80,'#f8fafc','#64748b')
txt(2245,1113,['Operations Team'],'head')
txt(2245,1138,['Incident response'],'small')
line([(2245,870),(2245,920)],'#ea580c',2.5,'arrow-orange')
line([(2245,1025),(2245,1080)],'#e11d48',2.5,'arrow-slate')
# monitoring connectors from VPC and edge to CW
line([(1825,575),(1975,575),(1975,755),(2010,755)],'#ea580c',2,'arrow-orange','7,6')
line([(1850,1210),(1975,1210),(1975,850),(2010,850)],'#ea580c',2,'arrow-orange','7,6')
line([(1140,210),(1945,210),(1945,735),(2010,735)],'#ea580c',1.8,'arrow-orange','7,6')
label(1960,700,'Metrics / logs')

# Footnotes
text_y = 1393
txt(55,text_y,'Design note: Route 53 Alias targets CloudFront in this recommended path. CloudFront WAF is associated with the distribution; it is not a separate network hop.','tiny','start')

out.append('</svg>')
svg=''.join(out)
base=Path(__file__).parent
(base/'architecture.svg').write_text(svg, encoding='utf-8')
cairosvg.svg2png(bytestring=svg.encode(), write_to=str(base/'architecture.png'), output_width=2540, output_height=1420)
print('Wrote architecture.svg and architecture.png')
