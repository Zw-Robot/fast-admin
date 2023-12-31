<script setup lang="ts">
import { ref, reactive } from "vue";
import Motion from "../utils/motion";
import { updateRules } from "../utils/rule";
import type { FormInstance } from "element-plus";
import { useVerifyCode } from "../utils/verifyCode";
import Lock from "@iconify-icons/ri/lock-fill";
import Iphone from "@iconify-icons/ep/iphone";
import User from "@iconify-icons/ri/user-3-fill";

import { message } from "@/utils/message";
import { useUserStoreHook } from "@/store/modules/user";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import { getTopMenu, initRouter } from "@/router/utils";
import router from "@/router";

const checked = ref(false);
const loading = ref(false);
const ruleForm = reactive({
  username: "",
  phone: "",
  // verifyCode: "",
  email: "",
  password: "",
  repeatPassword: ""
});
const ruleFormRef = ref<FormInstance>();
const { isDisabled, text } = useVerifyCode();
const repeatPasswordRule = [
  {
    validator: (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入确认密码"));
      } else if (ruleForm.password !== value) {
        callback(new Error("两次密码不一致!"));
      } else {
        callback();
      }
    },
    trigger: "blur"
  }
];

const onUpdate = async (formEl: FormInstance | undefined) => {
  loading.value = true;
  if (!formEl) return;
  await formEl.validate((valid, fields) => {
    if (valid) {
      if (checked.value) {
        useUserStoreHook()
          .signByUsername({
            username: ruleForm.username,
            password: ruleForm.password,
            phone: ruleForm.phone,
            email: ruleForm.email
          })
          .then(res => {
            if (res.success) {
              // 获取后端路由
              initRouter().then(() => {
                router.push(getTopMenu(true).path);
                message("登录成功", { type: "success" });
              });
            } else {
              loading.value = false;
              message("登录失败!" + " " + res.msg, { type: "error" });
            }
          });
        loading.value = false;
      } else {
        loading.value = false;
        message("请勾选隐私政策", { type: "warning" });
      }
    } else {
      loading.value = false;
      return fields;
    }
  });
};

function onBack() {
  useVerifyCode().end();
  useUserStoreHook().SET_CURRENTPAGE(0);
}
</script>

<template>
  <el-form
    ref="ruleFormRef"
    :model="ruleForm"
    :rules="updateRules"
    size="large"
  >
    <Motion>
      <el-form-item
        :rules="[
          {
            required: true,
            message: '请输入账号',
            trigger: 'blur'
          }
        ]"
        prop="username"
      >
        <el-input
          v-model="ruleForm.username"
          clearable
          placeholder="账号"
          :prefix-icon="useRenderIcon(User)"
        />
      </el-form-item>
    </Motion>

    <Motion :delay="100">
      <el-form-item prop="phone">
        <el-input
          v-model="ruleForm.phone"
          clearable
          placeholder="手机号码"
          :prefix-icon="useRenderIcon(Iphone)"
        />
      </el-form-item>
    </Motion>

<!--    <Motion :delay="150">-->
<!--      <el-form-item prop="verifyCode">-->
<!--        <div class="w-full flex justify-between">-->
<!--          <el-input-->
<!--            v-model="ruleForm.verifyCode"-->
<!--            clearable-->
<!--            placeholder="短信验证码"-->
<!--            :prefix-icon="useRenderIcon('ri:shield-keyhole-line')"-->
<!--          />-->
<!--          <el-button-->
<!--            :disabled="isDisabled"-->
<!--            class="ml-2"-->
<!--            @click="useVerifyCode().start(ruleFormRef, 'phone')"-->
<!--          >-->
<!--            {{ text.length > 0 ? text + "秒后重新获取" : "获取验证码" }}-->
<!--          </el-button>-->
<!--        </div>-->
<!--      </el-form-item>-->
<!--    </Motion>-->
    <Motion :delay="150">
      <el-form-item prop="email">
        <el-input
          v-model="ruleForm.email"
          clearable
          placeholder="邮箱"
          :prefix-icon="useRenderIcon('ep:message')"
        />
      </el-form-item>
    </Motion>

    <Motion :delay="200">
      <el-form-item prop="password">
        <el-input
          v-model="ruleForm.password"
          clearable
          show-password
          placeholder="密码"
          :prefix-icon="useRenderIcon(Lock)"
        />
      </el-form-item>
    </Motion>

    <Motion :delay="250">
      <el-form-item :rules="repeatPasswordRule" prop="repeatPassword">
        <el-input
          v-model="ruleForm.repeatPassword"
          clearable
          show-password
          placeholder="确认密码"
          :prefix-icon="useRenderIcon(Lock)"
        />
      </el-form-item>
    </Motion>

    <Motion :delay="300">
      <el-form-item>
        <el-checkbox v-model="checked"> 我已仔细阅读并接受 </el-checkbox>
        <el-button link type="primary"> 《隐私政策》 </el-button>
      </el-form-item>
    </Motion>

    <Motion :delay="350">
      <el-form-item>
        <el-button
          class="w-full"
          size="default"
          type="primary"
          :loading="loading"
          @click="onUpdate(ruleFormRef)"
        >
          确定
        </el-button>
      </el-form-item>
    </Motion>

    <Motion :delay="400">
      <el-form-item>
        <el-button class="w-full" size="default" @click="onBack">
          返回
        </el-button>
      </el-form-item>
    </Motion>
  </el-form>
</template>
