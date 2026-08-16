import { StyleSheet, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

import { Colors } from "../configs/Theme";

const ScreenContainer = ({children, withHeader = false, style}) => {
    const edges = withHeader ? ["left", "right", "bottom"] : ["top", "left", "right", "bottom"];

    return (
        <SafeAreaView edges={edges} style={styles.safeArea}>
            <View style={[styles.container, style]}>{children}</View>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    safeArea: {flex: 1, backgroundColor: Colors.background},
    container: {flex: 1}
});

export default ScreenContainer;
