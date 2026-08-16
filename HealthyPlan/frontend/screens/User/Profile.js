import { Alert, ScrollView, Text, View } from "react-native";
import { useContext } from "react";
import Ionicons from "@expo/vector-icons/Ionicons";

import AppButton from "../../components/AppButton";
import ScreenContainer from "../../components/ScreenContainer";
import SectionCard from "../../components/SectionCard";
import { MyUserContext } from "../../configs/Contexts";
import { Colors } from "../../configs/Theme";
import styles from "./Style";

const Profile = ({navigation}) => {
    const {user, healthProfile, logout} = useContext(MyUserContext);
    const fullName = [user?.last_name, user?.first_name].filter(Boolean).join(" ") || user?.username;

    const confirmLogout = () => {
        Alert.alert("Đăng xuất", "Bạn có chắc muốn đăng xuất khỏi HealthyPlan?", [
            {text: "Hủy", style: "cancel"},
            {text: "Đăng xuất", style: "destructive", onPress: logout}
        ]);
    }

    const InfoRow = ({icon, label, value}) => (
        <View style={styles.infoRow}>
            <Ionicons name={icon} size={20} color={Colors.primary} style={styles.infoIcon} />
            <View style={styles.infoContent}>
                <Text style={styles.infoLabel}>{label}</Text>
                <Text style={styles.infoValue}>{value || "Chưa cập nhật"}</Text>
            </View>
        </View>
    );

    return (
        <ScreenContainer>
            <ScrollView showsVerticalScrollIndicator={false}>
                <View style={styles.profileHeader}>
                    <View style={styles.avatar}><Ionicons name="person" size={42} color={Colors.primary} /></View>
                    <Text style={styles.profileName}>{fullName}</Text>
                    <Text style={styles.profileUsername}>@{user?.username}</Text>
                </View>
                <View style={styles.content}>
                    <SectionCard title="Thông tin tài khoản" icon="person-circle-outline" style={styles.cardSpacing}>
                        <InfoRow icon="mail-outline" label="Email" value={user?.email} />
                        <InfoRow icon="shield-checkmark-outline" label="Vai trò" value={user?.role === "customer" ? "Khách hàng" : user?.role} />
                        <AppButton title="Cập nhật thông tin" icon="create-outline" variant="secondary" onPress={() => navigation.navigate("UpdateUser")} style={styles.actionButton} />
                    </SectionCard>
                    <SectionCard title="Hồ sơ sức khỏe" icon="fitness-outline" style={styles.cardSpacing}>
                        <Text style={styles.infoValue}>{healthProfile ? "Hồ sơ đã được thiết lập" : "Chưa có hồ sơ sức khỏe"}</Text>
                        <AppButton title="Xem hồ sơ sức khỏe" icon="heart-outline" variant="secondary" onPress={() => navigation.navigate("HealthProfileDetails")} style={styles.actionButton} />
                    </SectionCard>
                    <SectionCard title="Thông tin ứng dụng" icon="information-circle-outline" style={styles.cardSpacing}>
                        <InfoRow icon="leaf-outline" label="Ứng dụng" value="HealthyPlan 1.0.0" />
                        <InfoRow icon="phone-portrait-outline" label="Nền tảng" value="Expo SDK 54" />
                    </SectionCard>
                    <AppButton title="Đăng xuất" icon="log-out-outline" variant="danger" onPress={confirmLogout} />
                </View>
            </ScrollView>
        </ScreenContainer>
    );
}

export default Profile;
