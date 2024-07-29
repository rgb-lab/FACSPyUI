from PyQt5.QtWidgets import (QMenuBar, QAction, QMessageBox)

from anndata import AnnData

from ._filehandler import FileHandler

from ._analysis_menus import (
    EditMetadataWindow,
    EditPanelWindow,
    EditCofactorTableWindow,
    SubsampleDatasetWindow,
    EqualizeGroupSizesWindow,
    SubsetGateWindow,
    LogicleTransformationWindow,
    HyperlogTransformationWindow,
    AsinhTransformationWindow,
    LogTransformationWindow,
    CalculateCofactorsWindow,
    SinglecellPCAWindow,
    SinglecellUMAPWindow,
    SinglecellTSNEWindow,
    SinglecellDiffmapWindow,
    SinglecellNeighborsWindow,
    SamplewisePCAWindow,
    SamplewiseMDSWindow,
    SamplewiseUMAPWindow,
    SamplewiseTSNEWindow,
    LeidenWindow,
    ParcWindow,
    PhenographWindow,
    FlowsomWindow,
    ScanoramaWindow,
    HarmonyWindow,
    GateFrequencyWindow,
    MFIWindow,
    FOPWindow
)


class MenuBar(QMenuBar, FileHandler):
    def __init__(self, main_window):
        QMenuBar.__init__(self, main_window)
        self.set_main_window(main_window)  # Set the main window for FileHandler
        self.init_menus()

    def init_menus(self):
        # File menu
        file_menu = self.addMenu("File")
        new_dataset_action = QAction("Create New Dataset", self)
        new_dataset_action.triggered.connect(self.create_new_dataset)
        file_menu.addAction(new_dataset_action)

        file_menu.addSeparator()

        open_action = QAction("Open...", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Save...", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        # Edit menu
        edit_menu = self.addMenu("Edit")
        edit_metadata_action = QAction("Edit Metadata", self)
        edit_metadata_action.triggered.connect(self.edit_metadata)
        edit_panel_action = QAction("Edit Panel", self)
        edit_panel_action.triggered.connect(self.edit_panel)
        edit_cofactor_action = QAction("Edit Cofactor Table", self)
        edit_cofactor_action.triggered.connect(self.edit_cofactor_table)

        subsample_action = QAction("Subsample data", self)
        subsample_action.triggered.connect(self.subsample_dataset)
        equalize_action = QAction("Equalize group sizes", self)
        equalize_action.triggered.connect(self.equalize_group_sizes)
        subset_gate_action = QAction("Subset gate", self)
        subset_gate_action.triggered.connect(self.subset_gate)

        edit_menu.addAction(edit_metadata_action)
        edit_menu.addAction(edit_panel_action)
        edit_menu.addAction(edit_cofactor_action)
        edit_menu.addSeparator()
        edit_menu.addAction(subsample_action)
        edit_menu.addAction(equalize_action)
        edit_menu.addAction(subset_gate_action)

        # Expression Menu
        expression_menu = self.addMenu("Expression metrics")
        mfi_action = QAction("Calculate marker intensity...", self)
        mfi_action.triggered.connect(self.calculate_mfi)
        fop_action = QAction("Calculate frequency of parent...", self)
        fop_action.triggered.connect(self.calculate_fop)

        expression_menu.addAction(mfi_action)
        expression_menu.addSeparator()
        expression_menu.addAction(fop_action)

        # Gating menu
        gating_menu = self.addMenu("Gating")
        calculate_gate_freqs = QAction("Calculate gate frequencies...", self)
        calculate_gate_freqs.triggered.connect(self.calc_gate_freqs)
        # supervised_action = QAction("Supervised gating", self)
        # supervised_action.triggered.connect(self.supervised_gating)
        # unsupervised_action = QAction("Unsupervised gating", self)
        # unsupervised_action.triggered.connect(self.unsupervised_gating)
        # manual_action = QAction("Manual gating", self)
        # manual_action.triggered.connect(self.manual_gating)

        gating_menu.addAction(calculate_gate_freqs)
        # gating_menu.addSeparator()
        # gating_menu.addAction(supervised_action)
        # gating_menu.addAction(unsupervised_action)
        # gating_menu.addAction(manual_action)

        # Transformation menu
        transformation_menu = self.addMenu("Transformation")
        cofactor_calc_action = QAction("Calculate Cofactors...", self)
        cofactor_calc_action.triggered.connect(self.calculate_cofactors)
        logicle_action = QAction("Run logicle...", self)
        logicle_action.triggered.connect(self.logicle)
        hyperlog_action = QAction("Run hyperlog...", self)
        hyperlog_action.triggered.connect(self.hyperlog)
        asinh_action = QAction("Run arcsinh...", self)
        asinh_action.triggered.connect(self.asinh)
        log_action = QAction("Run log...", self)
        log_action.triggered.connect(self.log)

        transformation_menu.addAction(cofactor_calc_action)
        transformation_menu.addSeparator()
        transformation_menu.addAction(logicle_action)
        transformation_menu.addAction(hyperlog_action)
        transformation_menu.addAction(asinh_action)
        transformation_menu.addAction(log_action)

        # Dimensionality reduction menu
        dimred_menu = self.addMenu("Dimensionality Reduction")
        sc_PCA_action = QAction("Run PCA...", self)
        sc_PCA_action.triggered.connect(self.sc_pca)
        neighbors_action = QAction("Run Neighbors...", self)
        neighbors_action.triggered.connect(self.neighbors)

        sc_umap_action = QAction("Run UMAP...", self)
        sc_umap_action.triggered.connect(self.sc_umap)
        sc_tsne_action = QAction("Run TSNE...", self)
        sc_tsne_action.triggered.connect(self.sc_tsne)
        sc_diffmap_action = QAction("Run Diffmap...", self)
        sc_diffmap_action.triggered.connect(self.sc_diffmap)

        sw_pca_action = QAction("Run Samplewise PCA...", self)
        sw_pca_action.triggered.connect(self.sw_pca)
        sw_umap_action = QAction("Run Samplewise UMAP...", self)
        sw_umap_action.triggered.connect(self.sw_umap)
        sw_tsne_action = QAction("Run Samplewise TSNE...", self)
        sw_tsne_action.triggered.connect(self.sw_tsne)
        sw_diffmap_action = QAction("Run Samplewise MDS...", self)
        sw_diffmap_action.triggered.connect(self.sw_mds)

        dimred_menu.addAction(sc_PCA_action)
        dimred_menu.addAction(neighbors_action)
        dimred_menu.addSeparator()
        dimred_menu.addAction(sc_umap_action)
        dimred_menu.addAction(sc_tsne_action)
        dimred_menu.addAction(sc_diffmap_action)
        dimred_menu.addSeparator()
        dimred_menu.addAction(sw_pca_action)
        dimred_menu.addAction(sw_umap_action)
        dimred_menu.addAction(sw_tsne_action)
        dimred_menu.addAction(sw_diffmap_action)

        # Clustering menu
        clustering_menu = self.addMenu("Clustering")
        leiden_action = QAction("Run leiden...", self)
        leiden_action.triggered.connect(self.leiden)
        flowsom_action = QAction("Run flowsom...", self)
        flowsom_action.triggered.connect(self.flowsom)
        phenograph_action = QAction("Run phenograph...", self)
        phenograph_action.triggered.connect(self.phenograph)
        parc_action = QAction("Run parc...", self)
        parc_action.triggered.connect(self.parc)

        clustering_menu.addAction(leiden_action)
        clustering_menu.addAction(flowsom_action)
        clustering_menu.addAction(parc_action)
        clustering_menu.addAction(phenograph_action)

        # # Integration menu
        # integration_menu = self.addMenu("Integration")
        # scanorama_action = QAction("Run scanorama...", self)
        # scanorama_action.triggered.connect(self.scanorama)
        # harmony_action = QAction("Run harmony...", self)
        # harmony_action.triggered.connect(self.harmony)

        # integration_menu.addAction(scanorama_action)
        # integration_menu.addAction(harmony_action)
    
    def scanorama(self):
        current_selection = self.check_if_dataset_is_selected()
        if current_selection:
            self.scanorama_window = ScanoramaWindow(self.main_window)
            self.scanorama_window.show()

    def harmony(self):
        current_selection = self.check_if_dataset_is_selected()
        if current_selection:
            self.harmony_window = HarmonyWindow(self.main_window)
            self.harmony_window.show()

    def leiden(self):
        current_selection = self.check_if_dataset_is_selected()
        if current_selection:
            self.leiden_window = LeidenWindow(self.main_window)
            self.leiden_window.show()
    def parc(self):
        current_selection = self.check_if_dataset_is_selected()
        if current_selection:
            self.parc_window = ParcWindow(self.main_window)
            self.parc_window.show()

    def phenograph(self):
        current_selection = self.check_if_dataset_is_selected()
        if current_selection:
            self.phenograph_window = PhenographWindow(self.main_window)
            self.phenograph_window.show()

    def flowsom(self):
        current_selection = self.check_if_dataset_is_selected()
        if current_selection:
            self.flowsom_window = FlowsomWindow(self.main_window)
            self.flowsom_window.show()

    def sc_pca(self):
        current_selection = self.check_if_dataset_is_selected()
        if current_selection:
            self.sc_pca_window = SinglecellPCAWindow(self.main_window)
            self.sc_pca_window.show()

    def neighbors(self):
        current_selection = self.check_if_dataset_is_selected()
        if current_selection:
            self.neighbors_window = SinglecellNeighborsWindow(self.main_window)
            self.neighbors_window.show()

    def sc_umap(self):
        current_selection = self.check_if_dataset_is_selected()
        if current_selection:
            self.sc_umap_window = SinglecellUMAPWindow(self.main_window)
            self.sc_umap_window.show()

    def sc_diffmap(self):
        current_selection = self.check_if_dataset_is_selected()
        if current_selection:
            self.sc_diffmap_window = SinglecellDiffmapWindow(self.main_window)
            self.sc_diffmap_window.show()

    def sc_tsne(self):
        current_selection = self.check_if_dataset_is_selected()
        if current_selection:
            self.sc_tsne_window = SinglecellTSNEWindow(self.main_window)
            self.sc_tsne_window.show()

    def sw_pca(self):
        current_selection = self.check_if_dataset_is_selected()
        if current_selection:
            self.sw_pca_window = SamplewisePCAWindow(self.main_window)
            self.sw_pca_window.show()

    def sw_umap(self):
        current_selection = self.check_if_dataset_is_selected()
        if current_selection:
            self.sw_umap_window = SamplewiseUMAPWindow(self.main_window)
            self.sw_umap_window.show()

    def sw_mds(self):
        current_selection = self.check_if_dataset_is_selected()
        if current_selection:
            self.sw_mds_window = SamplewiseMDSWindow(self.main_window)
            self.sw_mds_window.show()

    def sw_tsne(self):
        current_selection = self.check_if_dataset_is_selected()
        if current_selection:
            self.sw_tsne_window = SamplewiseTSNEWindow(self.main_window)
            self.sw_tsne_window.show()

    def calculate_cofactors(self):
        current_selection = self.check_if_dataset_is_selected()
        if current_selection:
            self.asinh_window = CalculateCofactorsWindow(self.main_window)
            self.asinh_window.show()

    def asinh(self):
        current_selection = self.check_if_dataset_is_selected()
        if current_selection:
            self.asinh_window = AsinhTransformationWindow(self.main_window)
            self.asinh_window.show()

    def log(self):
        current_selection = self.check_if_dataset_is_selected()
        if current_selection:
            self.log_window = LogTransformationWindow(self.main_window)
            self.log_window.show()

    def hyperlog(self):
        current_selection = self.check_if_dataset_is_selected()
        if current_selection:
            self.hyperlog_window = HyperlogTransformationWindow(self.main_window)
            self.hyperlog_window.show()

    def logicle(self):
        current_selection = self.check_if_dataset_is_selected()
        if current_selection:
            self.logicle_window = LogicleTransformationWindow(self.main_window)
            self.logicle_window.show()

    def edit_metadata(self):
        dataset, dataset_key = self.get_current_dataset()
        if 'metadata' in dataset.uns:
            metadata_df = dataset.uns["metadata"].to_df()
            self.edit_metadata_window = EditMetadataWindow(self.main_window, dataset_key, metadata_df)
            self.edit_metadata_window.show()
        else:
            QMessageBox.warning(self, "Warning", "No metadata found in the selected dataset.")

    def edit_panel(self):
        dataset, dataset_key = self.get_current_dataset()
        if 'panel' in dataset.uns:
            panel_df = dataset.uns["panel"].to_df()
            self.edit_panel_window = EditPanelWindow(self.main_window, dataset_key, panel_df)
            self.edit_panel_window.show()
        else:
            QMessageBox.warning(self, "Warning", "No panel found in the selected dataset.")

    def edit_cofactor_table(self):
        dataset, dataset_key = self.get_current_dataset()
        if 'cofactors' in dataset.uns:
            cofactor_df = dataset.uns["cofactors"].to_df()
            self.edit_cofactor_window = EditCofactorTableWindow(self.main_window, dataset_key, cofactor_df)
            self.edit_cofactor_window.show()
        else:
            QMessageBox.warning(self, "Warning", "No cofactor table found in the selected dataset.")

    def subsample_dataset(self):
        self.subsample_window = SubsampleDatasetWindow(self.main_window)
        self.subsample_window.show()

    def equalize_group_sizes(self):
        self.equalize_window = EqualizeGroupSizesWindow(self.main_window)
        self.equalize_window.show()

    def subset_gate(self):
        self.subset_window = SubsetGateWindow(self.main_window)
        self.subset_window.show()

    def calc_gate_freqs(self):
        current_selection = self.check_if_dataset_is_selected()
        if current_selection:
            self.gate_freq_window = GateFrequencyWindow(self.main_window)

    def calculate_mfi(self):
        current_selection = self.check_if_dataset_is_selected()
        if current_selection:
            self.mfi_window = MFIWindow(self.main_window)
            self.mfi_window.show()

    def calculate_fop(self):
        current_selection = self.check_if_dataset_is_selected()
        if current_selection:
            self.fop_window = FOPWindow(self.main_window)
            self.fop_window.show()

    def supervised_gating(self):
        QMessageBox.information(self, "Supervised gating", "Supervised gating clicked.")

    def unsupervised_gating(self):
        QMessageBox.information(self, "Unsupervised gating", "Unsupervised gating clicked.")

    def manual_gating(self):
        QMessageBox.information(self, "Manual gating", "Manual gating clicked.")

    def get_current_dataset(self) -> tuple[AnnData, str]:
        dataset_key = self.main_window.dataset_dropdown.currentText()
        if dataset_key in self.main_window.DATASHACK:
            return self.main_window.DATASHACK[dataset_key], dataset_key
        else:
            QMessageBox.warning(self, "Warning", "No dataset selected or invalid dataset.")
            return None, None

    def check_if_dataset_is_selected(self):
        x, y = self.get_current_dataset()
        if x is None and y is None:
            return False
        return True


