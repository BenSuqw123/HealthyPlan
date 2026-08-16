import { useContext } from "react";
import { View } from "react-native";
import Ionicons from "@expo/vector-icons/Ionicons";
import { StatusBar } from "expo-status-bar";
import { NavigationContainer } from "@react-navigation/native";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { SafeAreaProvider } from "react-native-safe-area-context";
import { enableScreens } from "react-native-screens";

import { ErrorView, LoadingView } from "./components/StateViews";
import { MyUserContext, MyUserProvider } from "./configs/Contexts";
import { Colors, NavigationTheme } from "./configs/Theme";
import Home from "./screens/Home/Home";
import Login from "./screens/User/Login";
import Profile from "./screens/User/Profile";
import Register from "./screens/User/Register";
import UpdateUser from "./screens/User/UpdateUser";
import HealthProfileDetails from "./screens/HealthProfile/HealthProfileDetails";
import HealthProfileForm from "./screens/HealthProfile/HealthProfileForm";
import GeneratePlan from "./screens/HealthPlan/GeneratePlan";
import HealthPlanDetails from "./screens/HealthPlan/HealthPlanDetails";
import HealthPlans from "./screens/HealthPlan/HealthPlans";
import FoodDetails from "./screens/Food/FoodDetails";
import Foods from "./screens/Food/Foods";
import ConsultationChat from "./screens/Consultation/ConsultationChat";
import ConsultationSessions from "./screens/Consultation/ConsultationSessions";

enableScreens();

const AuthStack = createNativeStackNavigator();
const SetupStack = createNativeStackNavigator();
const RootStack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

const screenOptions = {
    headerStyle: {backgroundColor: Colors.surface},
    headerTintColor: Colors.text,
    headerTitleStyle: {fontWeight: "700"},
    headerShadowVisible: false,
    contentStyle: {backgroundColor: Colors.background}
};

const AuthNavigator = () => (
    <AuthStack.Navigator screenOptions={{headerShown: false}}>
        <AuthStack.Screen name="Login" component={Login} />
        <AuthStack.Screen name="Register" component={Register} />
    </AuthStack.Navigator>
);

const SetupNavigator = () => (
    <SetupStack.Navigator screenOptions={{headerShown: false}}>
        <SetupStack.Screen name="SetupHealthProfile" component={HealthProfileForm} initialParams={{setup: true}} />
    </SetupStack.Navigator>
);

const tabIcons = {
    HomeTab: ["home", "home-outline"],
    HealthPlansTab: ["calendar", "calendar-outline"],
    ConsultationTab: ["chatbubbles", "chatbubbles-outline"],
    FoodsTab: ["nutrition", "nutrition-outline"],
    ProfileTab: ["person", "person-outline"]
};

const MainTabs = () => (
    <Tab.Navigator
        screenOptions={({route}) => ({
            headerShown: false,
            tabBarActiveTintColor: Colors.primary,
            tabBarInactiveTintColor: Colors.textSecondary,
            tabBarHideOnKeyboard: true,
            tabBarLabelStyle: {fontSize: 10, fontWeight: "600", paddingBottom: 2},
            tabBarStyle: {height: 66, paddingTop: 7, paddingBottom: 7, borderTopColor: Colors.border, backgroundColor: Colors.surface},
            tabBarIcon: ({focused, color, size}) => <Ionicons name={tabIcons[route.name][focused ? 0 : 1]} size={size} color={color} />
        })}
    >
        <Tab.Screen name="HomeTab" component={Home} options={{title: "Trang chủ"}} />
        <Tab.Screen name="HealthPlansTab" component={HealthPlans} options={{title: "Kế hoạch"}} />
        <Tab.Screen name="ConsultationTab" component={ConsultationSessions} options={{title: "Tư vấn"}} />
        <Tab.Screen name="FoodsTab" component={Foods} options={{title: "Thực phẩm"}} />
        <Tab.Screen name="ProfileTab" component={Profile} options={{title: "Cá nhân"}} />
    </Tab.Navigator>
);

const MainNavigator = () => (
    <RootStack.Navigator screenOptions={screenOptions}>
        <RootStack.Screen name="MainTabs" component={MainTabs} options={{headerShown: false}} />
        <RootStack.Screen name="GeneratePlan" component={GeneratePlan} options={{title: "Tạo kế hoạch"}} />
        <RootStack.Screen name="HealthPlanDetails" component={HealthPlanDetails} options={{title: "Chi tiết kế hoạch"}} />
        <RootStack.Screen name="FoodDetails" component={FoodDetails} options={{title: "Chi tiết thực phẩm"}} />
        <RootStack.Screen name="HealthProfileDetails" component={HealthProfileDetails} options={{title: "Hồ sơ sức khỏe"}} />
        <RootStack.Screen name="HealthProfileForm" component={HealthProfileForm} options={{title: "Cập nhật hồ sơ"}} />
        <RootStack.Screen name="ConsultationChat" component={ConsultationChat} options={{title: "Tư vấn sức khỏe"}} />
        <RootStack.Screen name="UpdateUser" component={UpdateUser} options={{title: "Cập nhật tài khoản"}} />
    </RootStack.Navigator>
);

const RootNavigator = () => {
    const {user, healthProfile, restoring, restoreError, restoreUserSession} = useContext(MyUserContext);

    if (restoring) return <View style={{flex: 1, backgroundColor: Colors.background}}><LoadingView message="Đang khôi phục phiên đăng nhập..." /></View>;
    if (restoreError) return <View style={{flex: 1, backgroundColor: Colors.background}}><ErrorView message={restoreError} onRetry={restoreUserSession} /></View>;
    if (!user) return <AuthNavigator />;
    if (!healthProfile) return <SetupNavigator />;
    return <MainNavigator />;
}

const App = () => {
    return (
        <SafeAreaProvider>
            <MyUserProvider>
                <NavigationContainer theme={NavigationTheme}>
                    <StatusBar style="dark" />
                    <RootNavigator />
                </NavigationContainer>
            </MyUserProvider>
        </SafeAreaProvider>
    );
}

export default App;
