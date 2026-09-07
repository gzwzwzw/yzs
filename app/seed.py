from app.auth import get_password_hash
from app.database import SessionLocal, engine, Base
from app import models


def init_db():
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # 如果已有数据则跳过
        if db.query(models.CulturalHistory).count() > 0:
            return
        # 创建管理员（如果不存在）
        admin_user = db.query(models.User).filter(models.User.username == "admin").first()
        if not admin_user:
            admin_user = models.User(
                username="admin",
                password_hash=get_password_hash("admin123"),  # 请修改默认密码
                    role="admin"
                )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
        # ===== 首页轮播图 =====
        banners = [
            models.HomeBanner(
                title="千年油纸伞，东方之美",
                image_url="/static/images/banner1.jpg",
                link_url="/history",
                sort_order=1
            ),
            models.HomeBanner(
                title="工艺传承，匠心独运",
                image_url="/static/images/banner2.jpg",
                link_url="/craft",
                sort_order=2
            ),
            models.HomeBanner(
                title="体验数字油纸伞",
                image_url="/static/images/banner3.jpg",
                link_url="/interactive",
                sort_order=3
            ),
        ]
        db.add_all(banners)

        # ===== 首页公告 =====
        announcements = [
            models.HomeAnnouncement(
                title="2026年油纸伞非遗文化展即将开幕",
                content="本次展览将展出各地油纸伞精品，并邀请传承人现场演示制作工艺。",
            ),
            models.HomeAnnouncement(
                title="油纸伞数字博物馆正式上线",
                content="足不出户，在线欣赏油纸伞之美。",
            ),
            models.HomeAnnouncement(
                title="研学活动报名开启",
                content="暑期油纸伞制作体验课程开始报名，名额有限。",
            ),
        ]
        db.add_all(announcements)

        # ===== 文化历史 =====
        histories = [
            models.CulturalHistory(
                title="油纸伞的起源",
                period="春秋战国",
                summary="油纸伞起源于中国，最早可追溯到春秋战国时期。",
                content="相传鲁班之妻云氏为丈夫遮阳避雨，仿照亭子制作了可收张的伞。后来蔡伦发明造纸术，人们用涂桐油的纸做伞面，称为油纸伞。",
                image_url="/static/images/history1.jpg",
                region="中国",
                sort_order=1
            ),
            models.CulturalHistory(
                title="唐宋时期的油纸伞",
                period="唐宋",
                summary="唐宋时期油纸伞在民间广泛使用，并传入日本、朝鲜等地。",
                content="唐代油纸伞成为日常用品，宋代出现彩色伞面，文人墨客常在伞面题诗作画。",
                image_url="/static/images/history2.jpg",
                region="中国",
                sort_order=2
            ),
            models.CulturalHistory(
                title="四川泸州油纸伞",
                period="明清至今",
                summary="泸州油纸伞制作技艺被列入国家级非物质文化遗产。",
                content="泸州油纸伞以手工精细、图案丰富著称，制作工序多达九十余道。其中以分水岭镇为最盛，其被誉为“中国油纸伞之乡”。",
                image_url="/static/images/history3.jpg",
                video_url="/static/videos/luzhou.mp4",
                region="四川泸州",
                sort_order=3
            ),
            models.CulturalHistory(
                title="浙江余杭油纸伞",
                period="明清至今",
                summary="余杭油纸伞以轻巧耐用闻名，是江南水乡的代表。",
                content="余杭油纸伞选用优质竹材和皮纸，伞面多绘有西湖风景、花鸟鱼虫。",
                image_url="/static/images/history4.jpg",
                region="浙江余杭",
                sort_order=4
            ),
        ]
        db.add_all(histories)

        # ===== 工艺步骤 =====
        craft_steps = [
            models.CraftStep(
                step_number=1,
                title="选竹",
                description="选用三年以上生长期的优质楠竹，要求竹节长、韧性好。",
                image_url="/static/images/craft1.jpg",
                material="楠竹",
                tool="砍刀、锯子",
                duration="1天"
            ),
            models.CraftStep(
                step_number=2,
                title="削伞骨",
                description="将竹子劈成细条，削成均匀的伞骨，长短一致。",
                image_url="/static/images/craft2.jpg",
                material="竹条",
                tool="篾刀、刨子",
                duration="2-3天"
            ),
            models.CraftStep(
                step_number=3,
                title="钻孔",
                description="在伞骨上钻出穿线孔，孔位必须精准对齐。",
                image_url="/static/images/craft3.jpg",
                tool="手钻",
                duration="1天"
            ),
            models.CraftStep(
                step_number=4,
                title="穿线组装",
                description="用棉线将伞骨串联，形成伞架结构。",
                image_url="/static/images/craft4.jpg",
                material="棉线",
                tool="针",
                duration="1天"
            ),
            models.CraftStep(
                step_number=5,
                title="裱伞面",
                description="将裁剪好的皮纸或宣纸粘贴在伞骨上，要求平整无皱。",
                image_url="/static/images/craft5.jpg",
                material="皮纸、浆糊",
                tool="刷子",
                duration="1-2天"
            ),
            models.CraftStep(
                step_number=6,
                title="绘花",
                description="在伞面绘制传统图案，如花鸟、山水、吉祥纹样。",
                image_url="/static/images/craft6.jpg",
                material="矿物颜料",
                tool="毛笔",
                duration="1-3天"
            ),
            models.CraftStep(
                step_number=7,
                title="上桐油",
                description="在伞面均匀涂刷桐油，使伞面防水、耐用、有光泽。",
                image_url="/static/images/craft7.jpg",
                material="桐油",
                tool="刷子",
                duration="1天"
            ),
            models.CraftStep(
                step_number=8,
                title="晾晒",
                description="将上好桐油的伞在通风处晾干，避免暴晒。",
                image_url="/static/images/craft8.jpg",
                duration="2-3天"
            ),
        ]
        db.add_all(craft_steps)

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    print("数据库初始化完成！")