# encoding:utf-8
from common.dy_glows import *
from common.login_check import *
from common.config import conf
from common.dy_badge import *
from common.logger import logger
import math
from common.get_secrets import get_secrets
from common.send_message import send_message


def run():
    logger.info("------登录检查开始------")
    login_res, login_exception_info = is_login()
    logger.info("------登录检查结束------")
    mode = int(conf.get_conf("Modechoose")['givemode'])
    if login_res:
        get_glow()
        try:
            glow_nums = get_own()
            assert glow_nums != 0
            if mode == 1:
                logger.info("当前选择模式为:自选模式")
                nums = conf.get_conf_list('selfMode', 'giftCount')
                room_list = conf.get_conf_list('selfMode', 'roomId')
                logger.info("------开始捐赠荧光棒------")
                for i in range(len(nums)):
                    glow_donate(nums[i], room_list[i])
                logger.info("------荧光棒捐赠结束------")
                messagetxt = "荧光棒捐赠结束"
                get_need_exp()
            elif mode == 0:
                logger.info("当前选择模式为:平均分配模式")
                room_list = get_room_list()
                every_give = math.ceil(glow_nums / len(room_list))
                left = int(glow_nums) - int(every_give) * (len(room_list) - 1)
                logger.info("------开始捐赠荧光棒------")
                for room in room_list:
                    if room == room_list[-1]:
                        glow_donate(left, room)
                    else:
                        glow_donate(every_give, room)
                logger.info("------荧光棒捐赠结束------")
                messagetxt = "荧光棒捐赠结束"
                get_need_exp()
            else:
                logger.warning("配置错误,没有这种选项,请修改配置并重新执行")
                messagetxt = "配置错误, 没有这种选项, 请修改配置并重新执行"
        except Exception as e:
            logger.warning("背包中没有荧光棒,无法执行赠送,任务即将结束")
            messagetxt = "背包中没有荧光棒, 无法执行赠送"
            logger.debug(e)
    else:
        if login_exception_info:
            messagetxt = f"未登录状态无法进行后续操作, 请检查Cookie有效性。登录检查时发生异常: {login_exception_info}"
        else:
            messagetxt = "未登录状态无法进行后续操作, 请检查Cookie有效性"
        logger.warning(messagetxt)
"""        
    try:

        server_key = get_secrets("SERVERPUSHKEY")
        if not (messagetxt == "荧光棒捐赠结束"):
            send_message(server_key, messagetxt)

    except Exception as e:
        logger.info("当前未配置Server酱推送，任务结束")
        logger.debug(e)
"""

if __name__ == '__main__':
    run()
