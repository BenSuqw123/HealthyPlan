import { useCallback, useContext, useState } from "react";
import { ActivityIndicator, Pressable, ScrollView, Text, View } from "react-native";
import Ionicons from "@expo/vector-icons/Ionicons";
import { useFocusEffect } from "@react-navigation/native";

import AppButton from "../../components/AppButton";
import ScreenContainer from "../../components/ScreenContainer";
import SectionCard from "../../components/SectionCard";
import Apis, { endpoints, getErrorMessage } from "../../configs/Apis";
import { MyUserContext } from "../../configs/Contexts";
import { Colors } from "../../configs/Theme";
import styles from "./Style";

const GOAL_LABELS = {lose_weight: "Giảm cân", maintain_weight: "Duy trì cân nặng", gain_weight: "Tăng cân"};
const ACTIVITY_LABELS = {sedentary: "Ít vận động", light: "Vận động nhẹ", moderate: "Vận động vừa", active: "Vận động nhiều", very_active: "Vận động rất nhiều"};

const Home = ({navigation}) => {
    const {user, healthProfile} = useContext(MyUserContext);
    const [latestPlan, setLatestPlan] = useState(null);
    const [planLoading, setPlanLoading] = useState(true);
    const [planError, setPlanError] = useState("");

    const loadLatestPlan = async () => {
        try {
            setPlanLoading(true);
            setPlanError("");
            const response = await Apis.get(endpoints.healthPlans);
            const plans = Array.isArray(response.data) ? response.data : [];
            plans.sort((first, second) => second.start_date.localeCompare(first.start_date));
            setLatestPlan(plans[0] || null);
        } catch (error) {
            setPlanError(getErrorMessage(error));
        } finally {
            setPlanLoading(false);
        }
    }

    useFocusEffect(useCallback(() => {
        loadLatestPlan();
    }, []));

    const getGreeting = () => {
        const hour = new Date().getHours();
        if (hour < 11) return "Chào buổi sáng";
        if (hour < 18) return "Chào buổi chiều";
        return "Chào buổi tối";
    }

    const displayName = user?.first_name || user?.username || "bạn";

    const QuickAction = ({icon, title, description, onPress}) => (
        <Pressable accessibilityRole="button" onPress={onPress} style={styles.quickAction}>
            <View style={styles.quickActionInner}>
                <View style={styles.quickIcon}><Ionicons name={icon} size={23} color={Colors.primary} /></View>
                <Text style={styles.quickTitle}>{title}</Text>
                <Text style={styles.quickDescription}>{description}</Text>
            </View>
        </Pressable>
    );

    return (
        <ScreenContainer>
            <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={styles.scroll}>
                <View style={styles.hero}>
                    <Text style={styles.eyebrow}>{getGreeting()},</Text>
                    <Text style={styles.greeting}>{displayName}</Text>
                    <Text style={styles.heroText}>Một lựa chọn lành mạnh hôm nay sẽ tạo nên thay đổi bền vững ngày mai.</Text>
                </View>
                <View style={styles.content}>
                    <SectionCard style={styles.overviewCard}>
                        <View style={styles.goalRow}>
                            <View style={styles.goalIcon}><Ionicons name="flag" size={24} color={Colors.primary} /></View>
                            <View>
                                <Text style={styles.goalLabel}>Mục tiêu hiện tại</Text>
                                <Text style={styles.goalValue}>{GOAL_LABELS[healthProfile?.goal] || "Chưa thiết lập"}</Text>
                            </View>
                        </View>
                        <View style={styles.metrics}>
                            <View style={[styles.metric, styles.metricSpacing]}><Text style={styles.metricValue}>{healthProfile?.weight || "--"} kg</Text><Text style={styles.metricLabel}>Cân nặng</Text></View>
                            <View style={[styles.metric, styles.metricSpacing]}><Text style={styles.metricValue}>{healthProfile?.height || "--"} cm</Text><Text style={styles.metricLabel}>Chiều cao</Text></View>
                            <View style={styles.metric}><Text numberOfLines={1} style={styles.metricValue}>{ACTIVITY_LABELS[healthProfile?.activity_level] || "--"}</Text><Text style={styles.metricLabel}>Vận động</Text></View>
                        </View>
                    </SectionCard>

                    <View style={styles.sectionHeader}><Text style={styles.sectionTitle}>Truy cập nhanh</Text></View>
                    <View style={styles.quickGrid}>
                        <QuickAction icon="restaurant-outline" title="Tạo kế hoạch" description="Lập thực đơn một ngày" onPress={() => navigation.navigate("GeneratePlan")} />
                        <QuickAction icon="chatbubbles-outline" title="Tư vấn" description="Hỏi trợ lý sức khỏe" onPress={() => navigation.navigate("ConsultationChat")} />
                        <QuickAction icon="nutrition-outline" title="Thực phẩm" description="Tra cứu dinh dưỡng" onPress={() => navigation.navigate("FoodsTab")} />
                        <QuickAction icon="heart-outline" title="Hồ sơ" description="Xem thông tin sức khỏe" onPress={() => navigation.navigate("HealthProfileDetails")} />
                    </View>

                    <View style={styles.sectionHeader}>
                        <Text style={styles.sectionTitle}>Kế hoạch gần nhất</Text>
                        <Pressable onPress={() => navigation.navigate("HealthPlansTab")}><Text style={styles.sectionLink}>Xem tất cả</Text></Pressable>
                    </View>
                    {planLoading ? <ActivityIndicator style={styles.planLoading} color={Colors.primary} /> : planError ? (
                        <View style={styles.planError}><Text style={styles.planErrorText}>{planError}</Text><Pressable onPress={loadLatestPlan}><Text style={styles.retryText}>Thử lại</Text></Pressable></View>
                    ) : latestPlan ? (
                        <Pressable onPress={() => navigation.navigate("HealthPlanDetails", {planId: latestPlan.id})}>
                            <SectionCard icon="calendar-outline" style={styles.planCard}>
                                <Text style={styles.planDate}>{latestPlan.start_date}</Text>
                                <Text style={styles.planTitle}>{latestPlan.title}</Text>
                                <Text style={styles.planMeta}>{latestPlan.meals?.length || 0} bữa ăn · Chạm để xem chi tiết</Text>
                            </SectionCard>
                        </Pressable>
                    ) : (
                        <View style={styles.emptyPlan}>
                            <Ionicons name="calendar-clear-outline" size={32} color={Colors.primary} />
                            <Text style={styles.emptyTitle}>Chưa có kế hoạch ăn uống</Text>
                            <Text style={styles.emptyText}>Tạo kế hoạch đầu tiên dựa trên hồ sơ sức khỏe của bạn.</Text>
                            <AppButton title="Tạo kế hoạch" onPress={() => navigation.navigate("GeneratePlan")} style={styles.emptyButton} />
                        </View>
                    )}
                </View>
            </ScrollView>
        </ScreenContainer>
    );
}

export default Home;
